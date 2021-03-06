from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['order_number', 'user', 'product_count',
                   'date', 'order_total', 'stripe_pid', 'address',
                   'original_bag', 'wh_success']
