from django.contrib import admin
from .models import FarmerOrder, Order, OrderLineItem, Address


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'order_total', 'stripe_pid', 'id',
                       'wh_success')

    fields = (
        'order_total', 'address', 'first_name',
        'last_name', 'phone_number', 'user', 'product_count',
    )

    list_display = ('order_number', 'date',
                    'order_total')

    ordering = ('-date',)


class OrderLineItemAdmin(admin.ModelAdmin):
    readonly_fields = ['order', 'farmer_order',
                       'product', 'quantity', 'delivery']


class FarmerOrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ['farmer', 'order']


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ['latitude', 'longitude', 'location']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLineItem, OrderLineItemAdmin)
admin.site.register(FarmerOrder, FarmerOrderAdmin)
admin.site.register(Address, AddressAdmin)
