from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
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

from geopy import distance


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
        product_list = []
        context = super().get_context_data(**kwargs)
        if 'user' in self.kwargs:
            user = self.kwargs['user']
            products = Product.objects.filter(created_by__id=user)
            for product in products:
                product_list.append({
                    'product': product,
                    'variants': ProductVariant.objects.filter(
                        product=product),
                })
            context['product_list'] = product_list
            return context
        products = context[self.context_object_name]
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            context['sort'] = sort
            if sort != 'distance':
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
                if sortkey:
                    products = products.order_by(sortkey)

        for product in products:
            product_list.append({
                'product': product,
                'variants': ProductVariant.objects.filter(
                    product=product),
            })
        if ('sort' in self.request.GET and
                'lat' in self.request.GET and
                'long' in self.request.GET):
            for item in product_list:
                user_location = (
                    self.request.GET['lat'], self.request.GET['long'])
                item_location = (
                    item['product'].created_by.profile.address.location)
                item['distance'] = round(distance.distance(
                    (item_location.coords[1], item_location.coords[0]),
                    user_location).km, 2)
                if item['distance'] < settings.DEFAULT_DELIVERY_RADIUS:
                    item['delivery'] = True
            product_list = sorted(product_list, key=lambda i: i['distance'])
        context['product_list'] = product_list
        if 'q' in self.request.GET:
            context['search_query'] = self.request.GET['q']
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


class ProductDelete(UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product-delete.html'
    raise_exception = True

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        messages.add_message(
            self.request,
            messages.ERROR,
            f'{object} deleted successfully.',
        )
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'products', kwargs={'user': self.request.user.id})

    def test_func(self):
        object = self.get_object()
        return object.created_by == self.request.user

    def handle_no_permission(self):
        obj = self.get_object()
        if obj.created_by != self.request.user:
            messages.add_message(
                self.request,
                messages.ERROR,
                'You can only delete your own products.',
            )
            return HttpResponseRedirect(reverse('home'))
