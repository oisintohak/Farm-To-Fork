from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from geopy import distance
from django.core.serializers import serialize
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from extra_views.advanced import InlineFormSetFactory, UpdateWithInlinesView
from accounts.models import UserModel
from .models import UserProfile
from checkout.models import Address
from .forms import UserProfileForm, AddressForm
from products.models import Product, ProductVariant
from multi_form_view import MultiModelFormView


class ProfileView(LoginRequiredMixin, DetailView):
    model = UserModel
    context_object_name = 'user_profile'
    template_name = 'profiles/profile-detail.html'

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            'Please log in to view profiles.',
        )
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(
            UserModel, id=self.kwargs.get('id'))

        if user.groups.filter(name='Farmers').exists():
            products = Product.objects.filter(created_by=user)
            product_list = {}
            for index, product in enumerate(products):
                product_list[index] = {
                    'product': product,
                    'variants': ProductVariant.objects.filter(
                        product=product),
                }
            context['product_list'] = product_list
        return context

    def get_object(self):
        user = get_object_or_404(
            UserModel, id=self.kwargs.get('id'))
        return user.profile


class ProfileEditView(LoginRequiredMixin, MultiModelFormView):
    form_classes = {
        'profile_form': UserProfileForm,
        'address_form': AddressForm,
    }
    template_name = 'profiles/profile-edit.html'
    raise_exception = True

    def get_objects(self):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        return {
            'profile_form': profile,
            'address_form': profile.address,
        }

    def get_success_url(self):
        return UserProfile.get_absolute_url(self)

    def forms_valid(self, all_forms):
        profile = all_forms['profile_form'].save(commit=False)
        profile.address = all_forms['address_form'].save()
        profile.save()
        return super().forms_valid(all_forms)

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            'Please log in to edit your profile.',
        )
        return super().handle_no_permission()


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
        markers = json.loads(
            serialize(
                'geojson',
                UserProfile.objects.filter(user__groups__name='Farmers'),
                geometry_field='location',
            )
        )
        for item in markers['features']:
            address = Address.objects.get(id=item['properties']['address'])
            if address.location:
                item['geometry'] = {
                    'type': 'Point',
                    'coordinates': [
                        address.location.coords[0],
                        address.location.coords[1]
                    ]
                }
        context['markers'] = markers
        return context
