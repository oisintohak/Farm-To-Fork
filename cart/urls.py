from django.urls import path
from .views import Cart, add_to_cart, update_cart

urlpatterns = [
    path('', Cart.as_view(), name='cart'),
    path('add/', add_to_cart, name='add-to-cart'),
    path('update/', update_cart, name='update_cart'),
]
