from django.contrib.auth.models import User
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import UserProfile


class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
