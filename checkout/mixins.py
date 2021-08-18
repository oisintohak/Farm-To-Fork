from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import redirect
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


class CheckoutAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Please login/register to place an order.',
            )
            self.redirect_field_name = self.request.path
            # return super().handle_no_permission()
            return redirect('%s?next=%s' % ('/accounts/login',
                                            self.request.get_full_path()))
            # return HttpResponseRedirect(reverse('account_login'))
        if self.request.user.profile.address.location is None:
            messages.add_message(
                self.request,
                messages.ERROR,
                'You need to add an address before placing an order.',
            )
            # self.redirect_field_name = 'profile-edit'
            # return super().handle_no_permission()
            # return HttpResponseRedirect(reverse('profile-edit'))
            return redirect('%s?next=%s' % ('/profiles/edit',
                                            self.request.get_full_path()))

    def test_func(self):
        return self.request.user.profile.address.location is not None
