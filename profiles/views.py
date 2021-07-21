from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from accounts.models import UserModel
from .models import UserProfile


class ProfileView(DetailView):
    model = UserModel
    context_object_name = 'user_profile'
    template_name = 'profiles/viewprofile.html'

    def get_object(self):
        user = get_object_or_404(
            UserModel, username=self.kwargs.get("username"))
        return user.profile


class ProfileEditView(UpdateView):
    model = UserProfile
    template_name = 'profiles/editprofile.html'
    fields = [
        'first_name',
        'last_name',
        'phone_number',
        'street_address1',
        'street_address2',
        'town_or_city',
        'county',
        'postcode',
        'country'
    ]

    def get_object(self):
        user = get_object_or_404(
            UserModel, username=self.kwargs.get("username"))
        return user.profile
