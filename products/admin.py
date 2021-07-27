from products.models import ProductVariant
from django.contrib import admin

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    fields = (
        'name', 'description', 'image_url', 'image',
        'unit_choices', 'price', 'size', 'unit',
        )


admin.site.register(ProductVariant, ProductAdmin)
