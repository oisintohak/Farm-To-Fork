from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, FormView
# from django.views.generic import ListView
# from django.views import View
from django.db import transaction
from django.contrib import messages
from django.forms import modelformset_factory, inlineformset_factory
from django.views.generic.edit import CreateView
from .models import ProductVariant, Product
from .forms import ProductForm, ProductVariantFormSet


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


class ProductCreate(CreateView):
    model = Product
    template_name = 'mycollections/collection_create.html'
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super(self).get_context_data(**kwargs)
        if self.request.POST:
            context['product_variant_formset'] = ProductVariantFormSet(
                self.request.POST)
        else:
            context['product_variant_formset'] = ProductVariantFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        variants = context['product_variant_formset']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if variants.is_valid():
                variants.instance = self.object
                variants.save()
        return super().form_valid(form)


def ProductEdit(request, product_id):
    product = Product.objects.get(id=product_id)
    ProductFormSet = inlineformset_factory(
        Product, ProductVariant, exclude=(), extra=0)
    if request.method == "POST":
        product_form = ProductForm(instance=product)
        formset = ProductFormSet(request.POST, request.FILES, instance=product)
        if formset.is_valid() and product_form.is_valid():
            formset.save()
            product_form.save()
            # Do something. Should generally end with a redirect. For example:
            return redirect(reverse('product', args=[product.id]))
        else:
            messages.error(
                request,
                ("Couldn't edit product. "
                 "Please check the form and try again")
            )
    else:
        product_form = ProductForm(instance=product)
        formset = ProductFormSet(instance=product)
    return render(
        request,
        'products/product-edit.html',
        {'formset': formset, 'product_form': product_form}
    )
