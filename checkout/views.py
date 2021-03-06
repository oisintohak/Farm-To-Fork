from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.contrib import messages

from multi_form_view import MultiModelFormView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Order, OrderLineItem, FarmerOrder
from profiles.models import UserProfile
from products.models import ProductVariant
from .forms import OrderForm
from profiles.forms import AddressForm
from .mixins import EmptyCartMixin
from cart.contexts import cart_contents

from allauth.account.views import SignupView
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from allauth.exceptions import ImmediateHttpResponse

from geopy import distance
import stripe
import json


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
        # IF A USER IS LOGGED IN, POPULATE THE ORDER FORM
        # WITH ANY EXISTING PROFILE DATA
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
        if order_cart['product_count'] == 0:
            messages.add_message(
                self.request,
                messages.ERROR,
                'No items in your cart.',
            )
            return redirect(reverse('cart'))
        for item in order_cart['cart_items']:
            # CALCULATE DISTANCE FOR EACH ITEM
            item_location = (
                item['product'].product.created_by.profile.address.location)
            dist = distance.distance(
                (item_location.coords[1], item_location.coords[0]),
                (order_location.coords[1], order_location.coords[0])).km
            item_distance = round(dist, 2)
            order_line_item = OrderLineItem(
                order=order,
                product=get_object_or_404(
                    ProductVariant, pk=item['product_id']),
                quantity=item['quantity'],
            )
            # FOR EACH LINE ITEM, CREATE OR UPDATE AN EXISTING FARMER ORDER
            # AND SET THE DISTANCE
            farmer_order, created = FarmerOrder.objects.update_or_create(
                order=order,
                farmer=item['product'].product.created_by
            )
            farmer_order.farmer = order_line_item.product.product.created_by
            farmer_order.distance = item_distance
            order_line_item.farmer_order = farmer_order
            # SET THE DELIVERY STATUS BASED ON DISTANCE
            if item_distance < settings.DEFAULT_DELIVERY_RADIUS:
                farmer_order.delivery = True
            order_line_item.save()
            farmer_order.save()
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
        farmer_orders = FarmerOrder.objects.filter(order=order)
        farmer_order_list = {}
        for index, farmer_order in enumerate(farmer_orders):
            farmer_order_list[index] = {
                'farmer_order': farmer_order,
                'line_items': OrderLineItem.objects.filter(
                    farmer_order=farmer_order)
            }
        context['farmer_order_list'] = farmer_order_list
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY
        context['stripe_public_key'] = stripe_public_key
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=int(round(order.order_total*100)),
            currency=settings.STRIPE_CURRENCY,
            metadata={
                'order_number': order.order_number,
                'username': self.request.user,
                'cart': json.dumps(self.request.session.get('cart', {})),
            }
        )
        pid = intent.client_secret.split('_secret')[0]
        order.stripe_pid = pid
        if self.request.user.is_authenticated:
            order.user = self.request.user
        order.save()
        context['client_secret'] = intent.client_secret
        return context

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        # REDIRECT TO ORDER DETAIL PAGE IF ORDER HAS BEEN PAID FOR
        if order.wh_success:
            messages.add_message(
                self.request,
                messages.ERROR,
                'This order has already been paid for.',
            )
            return redirect(reverse(
                'order-detail', kwargs={'order_number': order.order_number}))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        return redirect(reverse(
            'checkout-complete', kwargs={'order_number': order.order_number})
        )


class CheckoutComplete(TemplateView):
    """ A view to display the order details after payment."""
    template_name = 'checkout/checkout-complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        context['order'] = order
        context['order_line_items'] = OrderLineItem.objects.filter(order=order)
        farmer_orders = FarmerOrder.objects.filter(order=order)
        farmer_order_list = {}
        for index, farmer_order in enumerate(farmer_orders):
            farmer_order_list[index] = {
                'farmer_order': farmer_order,
                'line_items': OrderLineItem.objects.filter(
                    farmer_order=farmer_order)
            }
        context['farmer_order_list'] = farmer_order_list
        if 'cart' in self.request.session:
            del self.request.session['cart']
        return context


class Orders(LoginRequiredMixin, TemplateView):
    """
    A view to display all orders associated with a user.
    """
    template_name = 'checkout/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['my_orders'] = Order.objects.filter(user=user, wh_success=True)
        if user.groups.filter(name='Farmers').exists():
            context['farmer_orders'] = FarmerOrder.objects.filter(
                farmer=user, order__wh_success=True)
        return context


class RegisterWithOrder(SignupView):
    """
    Register a user and add an order and address to their account.
    This view can be accessed after an unauthenticated user places an order
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
        if not order.wh_success:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Error retrieving order.',
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


class OrderDetail(TemplateView):
    """
    A view to display all items in an order and delivery/collection
    status for each farmer within the order.
    """
    template_name = 'checkout/order-detail.html'

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        if not order.wh_success:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Error retrieving order.',
            )
            return HttpResponseRedirect(reverse('home'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        context['order'] = order
        farmer_orders = FarmerOrder.objects.filter(order=order)
        farmer_order_list = {}
        for index, farmer_order in enumerate(farmer_orders):
            farmer_order_list[index] = {
                'farmer_order': farmer_order,
                'line_items': OrderLineItem.objects.filter(
                    farmer_order=farmer_order)
            }
        context['farmer_order_list'] = farmer_order_list
        return context


class FarmerOrderDetail(TemplateView):
    """
    A view to display all items in a farmer order and
    the delivery/collection status.
    """
    template_name = 'checkout/farmer-order-detail.html'

    def get(self, request, *args, **kwargs):
        farmer_order = get_object_or_404(
            FarmerOrder, id=self.kwargs['id'])

        if not farmer_order.order.wh_success:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Error retrieving order.',
            )
            return HttpResponseRedirect(reverse('home'))
        elif self.request.user != farmer_order.farmer:
            messages.add_message(
                self.request,
                messages.ERROR,
                'This order is not assigned to your account.',
            )
            return HttpResponseRedirect(reverse('home'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(
            FarmerOrder, id=self.kwargs['id'])
        context['line_items'] = OrderLineItem.objects.filter(
            farmer_order=order)
        context['order'] = order
        return context
