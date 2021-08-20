from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class EmptyCartMixin(UserPassesTestMixin):
    """
    Mixin to redirect user to product list
    if there are no products in shopping cart.
    """

    raise_exception = True

    def handle_no_permission(self):
        if self.request.session.get('cart') == {}:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Nothing in your shopping cart.',
            )
            return redirect(reverse('product-list'))

    def test_func(self):
        return self.request.session.get('cart') != {}
