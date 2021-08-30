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

    fields = ('order_number', 'address', 'email',
              'first_name', 'last_name',
              'phone_number', 'user', 'date',
              'order_total', 'original_bag',
              'stripe_pid', 'product_count',
              'wh_success'
              )

    list_display = ('order_number', 'date',
                    'order_total')

    list_filter = ['wh_success']

    ordering = ('-date',)


class OrderLineItemAdmin(admin.ModelAdmin):
    readonly_fields = ['order', 'farmer_order',
                       'product', 'quantity', ]


class FarmerOrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    fields = ['farmer', 'order', 'farmer_order_total',
              'product_count', 'distance', 'delivery']
    readonly_fields = ['farmer', 'order']
    list_filter = ['farmer', 'order', 'delivery']



class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ['latitude', 'longitude', 'location']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLineItem, OrderLineItemAdmin)
admin.site.register(FarmerOrder, FarmerOrderAdmin)
admin.site.register(Address, AddressAdmin)
