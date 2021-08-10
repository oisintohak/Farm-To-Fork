from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import ListView
from extra_views import (
    CreateWithInlinesView,
    UpdateWithInlinesView,
    InlineFormSetFactory
)
from .models import ProductVariant, Product
from accounts.models import UserModel
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


class ProductList(ListView):
    model = Product
    template_name = 'products/product-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        product_list = {}
        for index, product in enumerate(products):
            product_list[index] = {
                'product': product,
                'variants': ProductVariant.objects.filter(
                    product=product),
                'owner': get_object_or_404(UserModel, pk=product.created_by.id)
            }

        context['product_list'] = product_list
        for item in product_list.values():
            print()
            print(item)
        return context


class ProductVariantInline(InlineFormSetFactory):
    model = ProductVariant
    factory_kwargs = {
        'extra': 1,
        'can_delete': True,
    }
    fields = ['price', 'size', 'unit', ]
    exclude = ['product', 'id']


class ProductCreate(
    LoginRequiredMixin, UserPassesTestMixin, CreateWithInlinesView
):
    model = Product
    inlines = [ProductVariantInline]
    fields = ['name', 'description', 'image_url', 'image']
    template_name = 'products/product-edit.html'
    raise_exception = True

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            'Login to a farmer account to create products.',
        )
        return HttpResponseRedirect(('/accounts/login/'))

    def test_func(self):
        return self.request.user.groups.filter(name='Farmers').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['helper'] = ProductVariantFormHelper()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductEdit(
    LoginRequiredMixin, UserPassesTestMixin, UpdateWithInlinesView
):
    model = Product
    inlines = [ProductVariantInline]
    fields = ['name', 'description', 'image_url', 'image']
    template_name = 'products/product-edit.html'
    raise_exception = True

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            'You can only edit your own products.',
        )
        return HttpResponseRedirect(reverse('home'))

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['helper'] = ProductVariantFormHelper()
        return context
