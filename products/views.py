from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views import View
from django.forms import modelformset_factory, inlineformset_factory
from .models import ProductVariant, Product
from .forms import ProductForm, ProductVariantFormSet


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


def ProductEditView(request, product_id):
    product = Product.objects.get(id=product_id)
    ProductFormSet = inlineformset_factory(Product, ProductVariant, exclude=())
    if request.method == "POST":
        product_form = ProductForm(instance=product)
        formset = ProductFormSet(request.POST, request.FILES, instance=product)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return redirect('')
    else:
        product_form = ProductForm(instance=product)
        formset = ProductFormSet(instance=product)
    return render(
        request,
        'products/editproduct.html',
        {'formset': formset, 'product_form': product_form}
    )


# class ProductEditView(FormView):
#     template_name = 'products/editproduct.html'

#     def get_initial(self):
#         super().get_initial()
#         product = get_object_or_404(
#             Product, id=self.kwargs.get('product_id'))
#         return product

#     def get_form_class(self):
#         ProductFormset = inlineformset_factory(
#             Product, ProductVariant, exclude=())
#         product = get_object_or_404(
#             Product, id=self.kwargs.get('product_id'))
#         formset = ProductFormset
#         return formset

#     def post(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#         formset = self.get_form_class()
#         if formset.is_valid():
#             formset.save()
#             # Do something. Should generally end with a redirect. For example:
#             return render(request, 'products/editproduct.html', {'formset': formset})

#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#         formset = self.get_form_class()
#         return render(request, 'products/editproduct.html', {'formset': formset})
