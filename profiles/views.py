from django.shortcuts import get_object_or_404
import json
from django.core.serializers import serialize
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from accounts.models import UserModel
from .models import UserProfile
from .forms import UserProfileForm


class ProfileView(DetailView):
    model = UserModel
    context_object_name = 'user_profile'
    template_name = 'profiles/viewprofile.html'

    def get_object(self):
        user = get_object_or_404(
            UserModel, username=self.kwargs.get('username'))
        return user.profile


class ProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profiles/editprofile.html'

    def get_object(self):
        user = get_object_or_404(
            UserModel, username=self.kwargs.get('username'))
        return user.profile


class FarmerMapView(TemplateView):
    template_name = 'profiles/farmermap.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["markers"] = json.loads(
            serialize(
                "geojson",
                UserProfile.objects.all(),
                geometry_field='location'
            )
        )
        return context
