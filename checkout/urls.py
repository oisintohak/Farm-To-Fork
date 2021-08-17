from django.urls import path
from .views import Checkout

urlpatterns = [
    path('', Checkout.as_view(), name='checkout'),
]
