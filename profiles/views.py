from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from accounts.models import UserModel
from .models import UserProfile
from .forms import UserProfileForm


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
    form_class = UserProfileForm
    template_name = 'profiles/editprofile.html'

    def get_object(self):
        user = get_object_or_404(
            UserModel, username=self.kwargs.get("username"))
        return user.profile
