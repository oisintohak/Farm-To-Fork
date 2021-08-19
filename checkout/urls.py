from django.urls import path
from .views import Checkout, Payment

urlpatterns = [
    path('', Checkout.as_view(), name='checkout'),
    path('payment', Payment.as_view(), name='payment'),
]
