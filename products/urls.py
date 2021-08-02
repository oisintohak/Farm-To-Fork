from django.urls import path
from .views import ProductDetail, ProductEdit, ProductCreate, ProductList

urlpatterns = [
    path('product/<pk>/', ProductDetail.as_view(), name='product-detail'),
    path('product-list/', ProductList.as_view(), name='product-list'),
    path('product-edit/<pk>/',
         ProductEdit.as_view(), name='product-edit'),
    path('product-create/',
         ProductCreate.as_view(), name='product-create'),

]
