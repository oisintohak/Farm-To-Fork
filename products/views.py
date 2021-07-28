from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .models import ProductVariant, Product
from .forms import ProductForm


class ProductView(DetailView):

    model = Product
    context_object_name = 'product'
    template_name = 'products/viewproduct.html'

    def get_object(self):
        product = get_object_or_404(
            Product, id=self.kwargs.get("id"))
        return product

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['variants'] = ProductVariant.objects.filter(
            product=self.get_object())
        return context


# class ProductCreateView(CreateView):


# class ProductEditView(UpdateView):
#     model = ProductVariant
#     form_class = ProductForm
#     template_name = 'profiles/editprofile.html'

#     def get_object(self):
#         product = get_object_or_404(
#             ProductVariant, id=self.kwargs.get("id"))
#         return product


# class ProductEditView(UpdateView):
#     model = ProductVariant
#     form_class = ProductForm
#     template_name = 'profiles/editprofile.html'

#     def get_object(self):
#         user = get_object_or_404(
#             UserModel, username=self.kwargs.get("username"))
#         return user.profile
