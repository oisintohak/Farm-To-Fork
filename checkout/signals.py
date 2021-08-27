from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order and farmer_order total on lineitem update/create
    """
    instance.order.update_total()
    instance.farmer_order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order and farmer_order total on lineitem delete
    """
    instance.farmer_order.update_total()
    instance.order.update_total()
