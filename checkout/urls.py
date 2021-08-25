from django.urls import path
from .views import (
    Checkout, Orders, Payment, CheckoutComplete, RegisterWithOrder
)

urlpatterns = [
    path('', Checkout.as_view(), name='checkout'),
    path('payment/<order_number>/', Payment.as_view(), name='payment'),
    path('complete/<order_number>/',
         CheckoutComplete.as_view(), name='checkout-complete'),
    path('orders', Orders.as_view(), name='orders'),
    path('register/<order_number>/', RegisterWithOrder.as_view(),
         name='register-with-order'),
]
