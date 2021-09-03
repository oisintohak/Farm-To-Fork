from django.contrib import admin
from .models import ProductVariant, Product

# Register your models here.


class ProductVariantAdminInline(admin.TabularInline):
    model = ProductVariant


class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductVariantAdminInline,)
    fields = (
        'name', 'description', 'image_url', 'image', 'created_by',
    )
    readonly_fields = ['id', 'created_by']


admin.site.register(Product, ProductAdmin)
