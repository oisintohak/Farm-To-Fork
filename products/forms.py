from django.forms import (
    modelform_factory, Form, ModelForm, inlineformset_factory
)
from .models import Product, ProductVariant


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductVariantForm(ModelForm):
    class Meta:
        model = ProductVariant
        fields = ('product', 'size', 'unit', 'price')
        # exclude = ['product']


ProductVariantFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    fields=('product', 'price', 'size', 'unit'),
    form=ProductVariantForm,
)

# ProductFormSet = modelform_factory(
#     Product,
#     ProductVariant,
#     fields=('price', 'size', 'unit'),
# )
