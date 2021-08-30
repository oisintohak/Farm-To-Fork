from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models.functions import Lower
from django.db.models import Q
from extra_views import (
    CreateWithInlinesView,
    UpdateWithInlinesView,
    InlineFormSetFactory
)
from .models import ProductVariant, Product
from .forms import ProductVariantFormHelper
from .mixins import ProductCreationAccessMixin, ProductEditAccessMixin


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = ProductVariant.objects.filter(
            product=self.get_object())
        return context


class Products(ListView):
    template_name = 'products/product-list.html'
    context_object_name = 'product_list'
    model = Product

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            return qs.filter(queries)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context[self.context_object_name]
        product_list = {}
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            context['sort'] = sort
            if sort == 'alpha':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sort == 'date':
                sortkey = 'created_at'
            if 'direction' in self.request.GET:
                direction = self.request.GET['direction']
                context['direction'] = direction
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
        for index, product in enumerate(products):
            product_list[index] = {
                'product': product,
                'variants': ProductVariant.objects.filter(
                    product=product),
            }
        context['product_list'] = product_list
        print(self.request.GET.copy())
        return context


class ProductVariantInline(InlineFormSetFactory):
    model = ProductVariant
    factory_kwargs = {
        'extra': 1,
        'can_delete': True,
        'max_num': 10
    }
    fields = ['price', 'size', 'unit', ]
    exclude = ['product', 'id']


class ProductCreate(
    LoginRequiredMixin,
    ProductCreationAccessMixin,
    CreateWithInlinesView,
):
    model = Product
    inlines = [ProductVariantInline]
    fields = ['name', 'description', 'image_url', 'image']
    template_name = 'products/product-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['helper'] = ProductVariantFormHelper()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductEdit(
    LoginRequiredMixin,
    ProductEditAccessMixin,
    UpdateWithInlinesView,
):
    model = Product
    inlines = [ProductVariantInline]
    fields = ['name', 'description', 'image_url', 'image']
    template_name = 'products/product-edit.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['helper'] = ProductVariantFormHelper()
        context['product'] = self.object
        return context
