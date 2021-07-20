from allauth.account.forms import SignupForm
from django import forms
from django.contrib import auth


class CustomSignupForm(SignupForm):
    """Extend the allauth Signup form to include a user_type field"""
    username = forms.CharField(max_length=20, label='Username', required=True)
    user_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[('Customers', 'Customer'), ('Farmers', 'Farmer')],
        label='Register as a:',
        required=True
    )

    class Meta:
        model = auth.get_user_model()

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.user_type = self.cleaned_data['user_type']
        user.save()
        profile = user.profile
        profile.save()

        return user
