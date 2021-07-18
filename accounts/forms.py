from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=40, label='First Name')
    last_name = forms.CharField(max_length=40, label='Last Name')
    username = forms.CharField(max_length=20, label='Username')
    user_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[('Customers', 'Customer'), ('Farmers', 'Farmer')],
        label='Register as a:')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
