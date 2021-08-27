import uuid
from django.db import models
from django.db.models import Sum
from django.db.models.fields import BooleanField
from products.models import ProductVariant
from django.contrib.gis.db.models import PointField

from django_countries.fields import CountryField


class Address(models.Model):
    street_address1 = models.CharField(max_length=80,
                                       null=True, blank=False)
    street_address2 = models.CharField(max_length=80,
                                       null=True, blank=False)
    town_or_city = models.CharField(max_length=40,
                                    null=True, blank=False)
    county = models.CharField(max_length=80,
                              null=True, blank=False)
    postcode = models.CharField(max_length=20,
                                null=True)
    country = CountryField(blank_label='Country',
                           null=True, blank=False)
    latitude = models.DecimalField(
        max_digits=30, decimal_places=20, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=30, decimal_places=20, blank=True, null=True
    )
    location = PointField(blank=True, null=True)


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    address = models.OneToOneField(
        Address,
        on_delete=models.SET_NULL,
        related_name='order',
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        default=None,
        null=True
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=40,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=40,
        null=True,
    )
    phone_number = models.CharField(max_length=20, null=False,
                                    blank=False, default=None)
    user = models.ForeignKey('accounts.UserModel', null=True,
                             blank=False, on_delete=models.SET_NULL,
                             related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')
    product_count = models.IntegerField(default=0)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.product_count = self.lineitems.aggregate(
            Sum('quantity'))['quantity__sum'] or 0
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return (f'Order of {self.product_count} '
                f'products for €{self.order_total} on '
                f'{self.date}')


class FarmerOrder(models.Model):
    farmer = models.ForeignKey('accounts.UserModel', null=True,
                               blank=False, on_delete=models.SET_NULL,
                               related_name='farmer_orders')
    order = models.OneToOneField(Order, null=False, blank=False,
                                 on_delete=models.CASCADE,
                                 related_name='farmer_orders')
    farmer_order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                             null=False, default=0)
    product_count = models.IntegerField(default=0)

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.farmer_order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.product_count = self.lineitems.aggregate(
            Sum('quantity'))['quantity__sum'] or 0
        self.save()

    def __str__(self):
        return (f'Order of {self.product_count} '
                f'products for €{self.farmer_order_total} on '
                f'{self.order.date}')


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    farmer_order = models.ForeignKey(FarmerOrder, null=False, blank=False,
                                     on_delete=models.CASCADE,
                                     related_name='lineitems', default=None)
    product = models.ForeignKey(ProductVariant, null=False, blank=False,
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)
    delivery = BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return ('Product variant id: '
                f'{self.product.id}, on '
                f'order number: {self.order.order_number}')
