from django.urls import path
from .views import Checkout, Payment, CheckoutComplete

urlpatterns = [
    path('', Checkout.as_view(), name='checkout'),
    path('payment/<order_number>/', Payment.as_view(), name='payment'),
    path('complete/<order_number>/', CheckoutComplete.as_view(), name='checkout-complete'),
]
