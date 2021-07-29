from django.urls import path
from .views import ProductDetail, ProductEdit

urlpatterns = [
    path('product/<id>/', ProductDetail.as_view(), name='product-detail'),
    path('product-edit/<product_id>/',
         ProductEdit, name='product-edit'),
]
