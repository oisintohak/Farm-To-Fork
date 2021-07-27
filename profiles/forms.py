from django.contrib.auth.models import User
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import UserProfile


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'street_address1',
            'street_address2',
            'town_or_city',
            'county',
            'postcode',
            'country',
            'latitude',
            'longitude',
        ]
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }