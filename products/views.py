from django.views.generic.detail import DetailView
from extra_views import (
    CreateWithInlinesView,
    UpdateWithInlinesView,
    InlineFormSetFactory
)
from .models import ProductVariant, Product
from .forms import ProductVariantFormHelper


class ProductDetail(DetailView):

    model = Product
    context_object_name = 'product'
    template_name = 'products/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = ProductVariant.objects.filter(
            product=self.get_object())
        return context


class ProductVariantInline(InlineFormSetFactory):
    model = ProductVariant
    factory_kwargs = {
        'extra': 1,
        'can_delete': True,
    }
    fields = ['price', 'size', 'unit', ]
    exclude = ['product', 'id']


class ProductCreate(CreateWithInlinesView):
    model = Product
    inlines = [ProductVariantInline]
    fields = ['name', 'description', 'image_url', 'image']
    template_name = 'products/product-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['helper'] = ProductVariantFormHelper()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductEdit(UpdateWithInlinesView):
    model = Product
    inlines = [ProductVariantInline]
    fields = ['name', 'description', 'image_url', 'image']
    template_name = 'products/product-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['helper'] = ProductVariantFormHelper()
        return context
