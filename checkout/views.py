from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib import messages

from .forms import OrderForm
from .mixins import CheckoutAccessMixin


class Checkout(
    CheckoutAccessMixin,
    LoginRequiredMixin,
    FormView
):

    form_class = OrderForm
    template_name = 'checkout/checkout.html'
