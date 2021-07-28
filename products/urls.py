from django.urls import path
from .views import ProductView, ProductEditView

urlpatterns = [
    path('product/<id>/', ProductView.as_view(), name='product'),
    path('edit-product/<product_id>/',
         ProductEditView, name='edit-product'),
]
