from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['order_number', 'user',
                   'date', 'order_total', 'stripe_pid', 'address']
