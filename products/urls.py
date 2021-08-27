from django.urls import path
from .views import (ProductDetail, ProductEdit, ProductCreate,
                    Products)

urlpatterns = [
    path('detail/<pk>/', ProductDetail.as_view(), name='product-detail'),
    path('', Products.as_view(), name='products'),
    path('create/', ProductCreate.as_view(), name='product-create'),
    path('edit/<pk>/', ProductEdit.as_view(), name='product-edit'),
]
