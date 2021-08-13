from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


class ProductCreationAccessMixin(UserPassesTestMixin):
    raise_exception = True

    def handle_no_permission(self):
        if not self.request.user.groups.filter(name='Farmers').exists():
            messages.add_message(
                self.request,
                messages.ERROR,
                'Login to a farmer account to create products.',
            )
            return HttpResponseRedirect(reverse('account_login'))
        if self.request.user.profile.location is None:
            messages.add_message(
                self.request,
                messages.ERROR,
                'You need to add an address before adding products.',
            )
            return HttpResponseRedirect(reverse('profile-edit'))

    def test_func(self):
        return (
            self.request.user.groups.filter(name='Farmers').exists() and
            self.request.user.profile.location is not None
        )


class ProductEditAccessMixin(ProductCreationAccessMixin, UserPassesTestMixin):
    raise_exception = True

    def handle_no_permission(self):
        ProductCreationAccessMixin.handle_no_permission(self)
        obj = self.get_object()
        if obj.created_by != self.request.user:
            messages.add_message(
                self.request,
                messages.ERROR,
                'You can only edit your own products.',
            )
            return HttpResponseRedirect(reverse('home'))

    def test_func(self):
        obj = self.get_object()
        return (
            ProductCreationAccessMixin.test_func(self) and
            obj.created_by == self.request.user
        )
