from django.urls import path
from .views import Cart, add_to_cart

urlpatterns = [
    path('', Cart.as_view(), name='cart'),
    path('add/', add_to_cart, name='add-to-cart'),
]
