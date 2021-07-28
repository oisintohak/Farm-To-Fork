from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views import View
from django.forms import modelformset_factory, inlineformset_factory
from .models import ProductVariant, Product
# from .forms import ProductForm, ProductVariantFormSet


class ProductView(DetailView):

    model = Product
    context_object_name = 'product'
    template_name = 'products/viewproduct.html'

    def get_object(self):
        product = get_object_or_404(
            Product, id=self.kwargs.get('id'))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = ProductVariant.objects.filter(
            product=self.get_object())
        return context

        formset = ProductFormset(instance=product)


class ProductEditView(FormView):
    def get_initial(self):
        super().get_initial()
        product = get_object_or_404(
            Product, id=self.kwargs.get('product_id'))
        return product

    def get_form_class(self):
        super().get_form_class()
        ProductFormset = inlineformset_factory(
            Product, ProductVariant, exclude=())
        formset = ProductFormset(instance=self.get_initial())
        return formset

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        formset = self.get_form_class()
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return render(request, '/products/editproduct.html', {'formset': formset})

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        formset = self.get_form_class()
        return render(request, '/products/editproduct.html', {'formset': formset})
