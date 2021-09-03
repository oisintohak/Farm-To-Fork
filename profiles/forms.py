from django import forms
from .models import UserProfile
from checkout.models import Address


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'bio',
            'image_url',
            'image',
        ]


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = [
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
