from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .forms import OrderForm
from .mixins import CheckoutAccessMixin
from multi_form_view import MultiModelFormView
from profiles.forms import AddressForm
from profiles.models import UserProfile


class Checkout(CheckoutAccessMixin,
               LoginRequiredMixin,
               MultiModelFormView):
    form_classes = {
        'order_form': OrderForm,
        'address_form': AddressForm,
    }
    template_name = 'checkout/checkout.html'
    raise_exception = True

    def get_objects(self):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        return {
            'order_form': None,
            'address_form': profile.address,
        }

    def forms_valid(self, all_forms):
        order = all_forms['profile_form'].save(commit=False)
        order.address = all_forms['address_form'].save()
        order.save()
        return super().forms_valid(all_forms)
