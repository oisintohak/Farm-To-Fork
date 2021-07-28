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

    ProductFormset = inlineformset_factory(Product, ProductVariant, exclude=())
        formset = ProductFormset(instance=product)


# class ProductEditView(FormView):
#     template_name = 'products/editproduct.html'
#     success_url = '/'

#     def get_form_class(self):
#         super().get_form_class()
#         product = get_object_or_404(
#             Product, id=self.kwargs.get('product_id'))
#         form_class = ProductVariantFormSet
#         return form_class

#     # def get_form_class(self):
#         # super().get_form_class()
#     #     product = get_object_or_404(
#     #         Product, id=self.kwargs.get('product_id'))
#     #     form_class = ProductVariantFormSet
#     #     return form_class

#     # def get_initial(self):
#     #     super().get_initial()
#     #     product = get_object_or_404(
#     #         Product, id=self.kwargs.get('product_id'))
#     #     return product

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         product = get_object_or_404(
#             Product, id=self.kwargs.get('product_id'))
#         # context['product_form'] = ProductForm(instance=product)
#         return context


def ProductEditView(request, product_id):
    product = Product.objects.get(pk=product_id)
    # LanguageFormset = modelformset_factory(Language, fields=('name',))
    ProductFormset = inlineformset_factory(Product, ProductVariant, exclude=())

    if request.method == 'POST':
        # formset = LanguageFormset(request.POST, queryset=Language.objects.filter(programmer__id=programmer.id))
        formset = ProductFormset(request.POST, instance=product)
        if formset.is_valid():
            formset.save()
            # instances = formset.save(commit=False)
            # for instance in instances:
            #    instance.programmer_id = programmer.id
            #    instance.save()

            return redirect('profile', username=request.user.username)

    # formset = LanguageFormset(queryset=Language.objects.filter(programmer__id=programmer.id))
    formset = ProductFormset(instance=product)

    return render(request, 'products/editproduct.html', {'formset': formset})


# class ProductEditView(FormView):
#     def get_initial(self):
#         super().get_initial()
#         product = Product.objects.filter(id=self.kwargs.get('id'))
#         # variants = ProductVariant.objects.filter(product=product)
#         return product

#     def get_form_class(self):
#         super().get_form_class()
#         ProductFormSet = inlineformset_factory(
#             Product, ProductVariant, exclude=())
#         formset = ProductFormSet(instance=self.get_initial())
#         return formset

#     template_name = 'products/editproduct.html'

    # class ProductCreateView(CreateView):

    #     model = ProductVariant
    #     form_class = ProductForm
    #     template_name = 'profiles/editprofile.html'

    #     def get_object(self):
    #         product = get_object_or_404(
    #             ProductVariant, id=self.kwargs.get('id'))
    #         return product

    # class ProductEditView(UpdateView):
    #     model = ProductVariant
    #     form_class = ProductForm
    #     template_name = 'profiles/editprofile.html'

    #     def get_object(self):
    #         user = get_object_or_404(
    #             UserModel, username=self.kwargs.get('username'))
    #         return user.profile
