from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from accounts.models import UserModel
from profiles.models import UserProfile
from products.models import Product, ProductVariant


class Home(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farmers'] = UserProfile.objects.filter(
            user__groups__name='Farmers')
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
        return context


class About(TemplateView):
    template_name = 'home/about.html'
