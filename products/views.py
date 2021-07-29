from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from extra_views import (
    CreateWithInlinesView,
    UpdateWithInlinesView,
    InlineFormSetFactory
)
from .models import ProductVariant, Product


class ProductDetail(DetailView):

    model = Product
    context_object_name = 'product'
    template_name = 'products/product-detail.html'

    def get_object(self):
        product = get_object_or_404(
            Product, id=self.kwargs.get('id'))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = ProductVariant.objects.filter(
            product=self.get_object())
        return context


class ProductVariantInline(InlineFormSetFactory):
    model = ProductVariant
    factory_kwargs = {'extra': 1}
    fields = ['price', 'size', 'unit']


class ProductCreate(CreateWithInlinesView):
    model = Product
    inlines = [ProductVariantInline]
    fields = ['name', 'description', 'image_url', 'image']
    template_name = 'products/product-edit.html'


class ProductEdit(UpdateWithInlinesView):
    model = Product
    inlines = [ProductVariantInline]
    fields = ['name', 'description', 'image_url', 'image']
    template_name = 'products/product-edit.html'
