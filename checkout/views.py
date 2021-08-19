from django.shortcuts import get_object_or_404
from .forms import OrderForm
from multi_form_view import MultiModelFormView
from profiles.forms import AddressForm
from profiles.models import UserProfile


class Checkout(MultiModelFormView):
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
            initial['order_form']['email'] = self.request.user.email
        return initial

    def get_objects(self):
        if self.request.user.is_authenticated:
            profile = get_object_or_404(UserProfile, user=self.request.user)
            initial_data = {
                'order_form': profile,
                'address_form': profile.address,
            }
            return initial_data
        else:
            return super().get_objects(self)

    def forms_valid(self, all_forms):
        order = all_forms['profile_form'].save(commit=False)
        order.address = all_forms['address_form'].save()
        order.save()
        return super().forms_valid(all_forms)
