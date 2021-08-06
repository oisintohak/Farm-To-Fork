from django.contrib import admin
from .models import ProductVariant, Product

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    fields = (
        'name', 'description', 'image_url', 'image', 'created_by',
    )
    readonly_fields = ['id']


class ProductVariantAdmin(admin.ModelAdmin):
    fields = (
        'product', 'price', 'size', 'unit',
    )
    readonly_fields = ['id']


admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Product, ProductAdmin)
