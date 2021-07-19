from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=40, label='First Name', required=True)
    last_name = forms.CharField(
        max_length=40, label='Last Name', required=True)
    username = forms.CharField(max_length=20, label='Username', required=True)
    user_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[('Customers', 'Customer'), ('Farmers', 'Farmer')],
        label='Register as a:',
        required=True
    )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = self.cleaned_data['user_type']
        user.extra_field = self.cleaned_data['extra_field']

        user.save()
