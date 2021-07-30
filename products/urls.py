from django.urls import path
from .views import ProductDetail, ProductEdit, ProductCreate

urlpatterns = [
    path('product/<pk>/', ProductDetail.as_view(), name='product-detail'),
    path('product-edit/<pk>/',
         ProductEdit.as_view(), name='product-edit'),
    path('product-create/',
         ProductCreate.as_view(), name='product-create'),

]
