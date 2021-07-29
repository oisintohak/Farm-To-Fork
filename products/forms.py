from django.forms import (
    modelform_factory, Form, ModelForm, inlineformset_factory
)
from .models import Product, ProductVariant


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ()


class ProductVariantForm(ModelForm):
    class Meta:
        model = ProductVariant
        exclude = ()


ProductVariantFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    fields=('product', 'price', 'size', 'unit'),
    form=ProductVariantForm,
)
