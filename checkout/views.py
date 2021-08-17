from django.views.generic.edit import FormView

from .forms import OrderForm


class Checkout(FormView):
    form_class = OrderForm
    template_name = 'checkout/checkout.html'
