from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.conf import settings
from multi_form_view import MultiModelFormView
from profiles.forms import AddressForm
from profiles.models import UserProfile
from .forms import OrderForm
from .mixins import EmptyCartMixin
from cart.contexts import cart_contents
from .models import Order

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
            initial['address_form']['street_address1'] = profile.address.street_address1
            initial['address_form']['street_address2'] = profile.address.street_address2
            initial['address_form']['town_or_city'] = profile.address.town_or_city
            initial['address_form']['county'] = profile.address.county
            initial['address_form']['postcode'] = profile.address.postcode
            initial['address_form']['country'] = profile.address.country
        return initial

    def forms_valid(self, all_forms):
        order = all_forms['order_form'].save(commit=False)
        print(type(order))
        order.address = all_forms['address_form'].save()
        order.save()
        print('order')
        print(order.order_number)
        return redirect(reverse('payment', kwargs={'order_number': order.order_number}))

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
        current_cart = cart_contents(self.request)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        context['stripe_secret_key'] = settings.STRIPE_SECRET_KEY

        stripe.api_key = 'sk_test_51J3J6ySIpQvL8FY5gm76sDjVWukN4NnOxZVrpcOuaOuCd5JNhrbE3uqroK0NCC7VRSNi8ygdwNhW5Jvrq4R846WD00NOLZcbtp'
        intent = stripe.PaymentIntent.create(
            amount=int(round(current_cart['total']*100)),
            currency=settings.STRIPE_CURRENCY,
        )
        context['client_secret'] = intent.client_secret

        context['order'] = get_object_or_404(
            Order, order_number=self.kwargs['order_number'])
        # print(intent)
        return context
