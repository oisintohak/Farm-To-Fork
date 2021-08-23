from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.conf import settings


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
        current_cart = cart_contents(self.request)
        order_location = order.address.location
        for item in current_cart['cart_items']:
            item['location'] = (
                item['product'].product.created_by.profile.address.location)
            item['distance'] = (
                distance.distance(item['location'], order_location).km)
            order_line_item = OrderLineItem(
                order=order,
                product=get_object_or_404(
                    ProductVariant, pk=item['product_id']),
                quantity=item['quantity'],
            )
            order_line_item.save()
        context['current_cart'] = current_cart
        context['order'] = order
        context['stripe_public_key'] = 'pk_test_51JRZbxKGBmFv7pxwQbENF9k0Qujo9ebBhLY1owB5HeqZEBOPx5KPCfvF8cwbHJp3XyiaEzGkz9g8dOunnkwQg6cG003rEknglB'
        context['stripe_secret_key'] = 'sk_test_51JRZbxKGBmFv7pxw1kFWuq2dtP0z4s7VMepVlOdsg1ttsGBoNSst5W1YsQVDyYrp2iCK6ODYXpyi1JtR5r1OqHKo00Hx4A5dsa'
        stripe.api_key = 'sk_test_51JRZbxKGBmFv7pxw1kFWuq2dtP0z4s7VMepVlOdsg1ttsGBoNSst5W1YsQVDyYrp2iCK6ODYXpyi1JtR5r1OqHKo00Hx4A5dsa'
        intent = stripe.PaymentIntent.create(
            amount=int(round(current_cart['total']*100)),
            currency=settings.STRIPE_CURRENCY,
        )
        context['client_secret'] = intent.client_secret
        return context

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        pid = request.POST.get('client_secret').split('_secret')[0]
        order.stripe_pid = pid
        order.save()
        return redirect(reverse('home'))
