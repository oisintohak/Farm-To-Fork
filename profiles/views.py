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
            UserModel, id=self.kwargs.get('id'))
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
    """
    Display a map with markers for farmer locations
    """
    template_name = 'profiles/farmermap.html'

    def get_context_data(self, **kwargs):
        """
        Add an array to context containing GeoJSON information about farmers
        """
        context = super().get_context_data(**kwargs)
        context["markers"] = json.loads(
            serialize(
                "geojson",
                UserProfile.objects.filter(user__groups__name='Farmers'),
                geometry_field='location'
            )
        )
        return context
