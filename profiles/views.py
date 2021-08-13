from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json
from django.core.serializers import serialize
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from accounts.models import UserModel
from .models import UserProfile
from .forms import UserProfileForm


class ProfileView(LoginRequiredMixin, DetailView):
    model = UserModel
    context_object_name = 'user_profile'
    template_name = 'profiles/profile-detail.html'

    def get_object(self):
        user = get_object_or_404(
            UserModel, id=self.kwargs.get('id'))
        return user.profile


class ProfileEditView(LoginRequiredMixin, UpdateView):
    # model = UserProfile
    form_class = UserProfileForm
    template_name = 'profiles/profile-edit.html'

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            'Please log in to edit your profile.',
        )
        return super().handle_no_permission()

    def get_object(self):
        user = self.request.user
        return user.profile


longitude = -80.191788
latitude = 25.761681

user_location = Point(longitude, latitude, srid=4326)


class FarmerList(ListView):
    model = UserProfile
    context_object_name = 'farmers'
    queryset = UserProfile.objects.filter(
        user__groups__name='Farmers'
    ).annotate(
        distance=Distance('location', user_location)
    ).order_by('distance')
    template_name = 'profiles/farmer-list.html'


class FarmerMapView(TemplateView):
    """
    Display a map with markers for farmer locations
    """
    template_name = 'profiles/farmer-map.html'

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
