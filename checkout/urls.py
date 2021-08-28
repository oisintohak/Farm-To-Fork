from django.urls import path
from .views import (
    Checkout, FarmerOrderDetail,
    OrderDetail, Orders, Payment,
    CheckoutComplete, RegisterWithOrder
)
from .webhooks import webhook

urlpatterns = [
    path('', Checkout.as_view(), name='checkout'),
    path('payment/<order_number>/', Payment.as_view(), name='payment'),
    path('complete/<order_number>/',
         CheckoutComplete.as_view(), name='checkout-complete'),
    path('orders', Orders.as_view(), name='orders'),
    path('order-detail/<order_number>',
         OrderDetail.as_view(), name='order-detail'),
    path('farmer-order-detail/<id>', FarmerOrderDetail.as_view(),
         name='farmer-order-detail'),
    path('register/<order_number>/', RegisterWithOrder.as_view(),
         name='register-with-order'),
    path('wh/', webhook, name='webhook'),

]
