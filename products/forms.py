from django.forms import modelform_factory
from .models import Product, ProductVariant


ProductForm = modelform_factory(
    ProductVariant, fields=('unit', 'price', 'size'))
