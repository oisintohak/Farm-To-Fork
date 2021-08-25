from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.contrib import messages


from profiles.forms import AddressForm
from profiles.models import UserProfile
from .forms import OrderForm
from .mixins import EmptyCartMixin
from cart.contexts import cart_contents
from .models import Order, OrderLineItem
from products.models import ProductVariant
from multi_form_view import MultiModelFormView
from geopy import distance
import stripe
from allauth.account.views import SignupView
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from allauth.exceptions import ImmediateHttpResponse


class Checkout(EmptyCartMixin, MultiModelFormView):
    """
    A view to display the checkout form, with order and address forms
    populated with profile data if a user is logged in
    """
    form_classes = {
        'order_form': OrderForm,
        'address_form': AddressForm,
    }
    template_name = 'checkout/checkout.html'

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            profile = get_object_or_404(UserProfile, user=self.request.user)
            initial['order_form']['email'] = self.request.user.email
            initial['order_form']['first_name'] = profile.first_name
            initial['order_form']['last_name'] = profile.last_name
            initial['order_form']['phone_number'] = profile.phone_number
            initial['address_form']['street_address1'] = (
                profile.address.street_address1)
            initial['address_form']['street_address2'] = (
                profile.address.street_address2)
            initial['address_form']['town_or_city'] = (
                profile.address.town_or_city)
            initial['address_form']['county'] = profile.address.county
            initial['address_form']['postcode'] = profile.address.postcode
            initial['address_form']['country'] = profile.address.country
        return initial

    def forms_valid(self, all_forms):
        order = all_forms['order_form'].save(commit=False)
        order.address = all_forms['address_form'].save()
        order.save()
        order_cart = cart_contents(self.request)
        order_location = order.address.location
        for item in order_cart['cart_items']:
            item_location = (
                item['product'].product.created_by.profile.address.location)
            item_distance = (
                distance.distance(item_location, order_location).km)
            order_line_item = OrderLineItem(
                order=order,
                product=get_object_or_404(
                    ProductVariant, pk=item['product_id']),
                quantity=item['quantity'],
            )
            if item_distance < settings.DEFAULT_DELIVERY_RADIUS:
                order_line_item.delivery = True
            order_line_item.save()
        return redirect(
            reverse('payment', kwargs={'order_number': order.order_number})
        )

    def get_success_url(self):
        return 'payment'


class Payment(EmptyCartMixin, TemplateView):
    """
    Display the stripe payment form and show the delivery
    or collection details for each product.
    """
    template_name = 'checkout/payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        context['order'] = order
        context['order_line_items'] = OrderLineItem.objects.filter(order=order)
        context['stripe_public_key'] = 'pk_test_51JRZbxKGBmFv7pxwQbENF9k0Qujo9ebBhLY1owB5HeqZEBOPx5KPCfvF8cwbHJp3XyiaEzGkz9g8dOunnkwQg6cG003rEknglB'
        context['stripe_secret_key'] = 'sk_test_51JRZbxKGBmFv7pxw1kFWuq2dtP0z4s7VMepVlOdsg1ttsGBoNSst5W1YsQVDyYrp2iCK6ODYXpyi1JtR5r1OqHKo00Hx4A5dsa'
        stripe.api_key = 'sk_test_51JRZbxKGBmFv7pxw1kFWuq2dtP0z4s7VMepVlOdsg1ttsGBoNSst5W1YsQVDyYrp2iCK6ODYXpyi1JtR5r1OqHKo00Hx4A5dsa'
        intent = stripe.PaymentIntent.create(
            amount=int(round(order.order_total*100)),
            currency=settings.STRIPE_CURRENCY,
        )
        context['client_secret'] = intent.client_secret
        return context

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        pid = request.POST.get('client_secret').split('_secret')[0]
        order.stripe_pid = pid
        if self.request.user.is_authenticated:
            order.user = self.request.user
        order.save()
        return redirect(reverse(
            'checkout-complete', kwargs={'order_number': order.order_number})
        )


class CheckoutComplete(TemplateView):
    template_name = 'checkout/checkout-complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        context['order'] = order
        context['order_line_items'] = OrderLineItem.objects.filter(order=order)
        if 'cart' in self.request.session:
            del self.request.session['cart']
        return context


class Orders(LoginRequiredMixin, TemplateView):
    template_name = 'checkout/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['my_orders'] = Order.objects.filter(user=user)
        incoming_orders = {}
        line_items = (
            OrderLineItem.objects.filter(product__product__created_by=user))
        for index, item in enumerate(line_items):
            incoming_orders[index] = {
                'order': Order.objects.filter(id=item.order.id),
                'line_items': line_items.filter(order=item.order)
            }
        context['incoming_orders'] = incoming_orders
        return context


class RegisterWithOrder(SignupView):
    """
    Register a user and add an order and address to their account
    """
    template_name = 'checkout/register-with-order.html'

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        if order.user:
            messages.add_message(
                self.request,
                messages.ERROR,
                'This order is was placed by another user.',
            )
            return HttpResponseRedirect(reverse('home'))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.user = form.save(self.request)
        
        # get the order and address and assign them to the new user
        order = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        order.user = self.user
        order.save()
        self.user.profile.address = order.address
        self.user.profile.save()
        
        # this is taken from the allauth SignupView
        try:
            return complete_signup(
                self.request,
                self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url(),
            )
        except ImmediateHttpResponse as e:
            return e.response
