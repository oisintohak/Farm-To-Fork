from django.urls import path
from .views import ProductDetail, ProductEdit, ProductCreate, ProductList

urlpatterns = [
    path('detail/<pk>/', ProductDetail.as_view(), name='product-detail'),
    path('', ProductList.as_view(), name='product-list'),
    path('create/', ProductCreate.as_view(), name='product-create'),
    path('edit/<pk>/', ProductEdit.as_view(), name='product-edit'),
]
