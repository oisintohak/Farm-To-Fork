from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Address, FarmerOrder, Order, OrderLineItem
from products.models import Product, ProductVariant
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_farmer_email(self, order):
        farmer_orders = FarmerOrder.objects.filter(order=order)
        farmer_order_list = {}
        for index, farmer_order in enumerate(farmer_orders):
            farmer_order_list[index] = {
                'farmer_order': farmer_order,
                'line_items': OrderLineItem.objects.filter(
                    farmer_order=farmer_order)
            }
        for farmer_order in farmer_order_list:
            with farmer_order.farmer_order.farmer as farmer:
                recipient = farmer.email
                subject = render_to_string
                (
                    'checkout/confirmation_emails/farmer_email_subject.txt',
                    {'order': farmer_order.farmer_order}
                )
                body_context = {'order': farmer_order.farmer_order,
                                'farmer': farmer,
                                'contact_email': settings.DEFAULT_FROM_EMAIL
                                }
                if farmer_order.farmer_order.delivery:
                    body_context['address'] = order.address
                    body_context['delivery'] = 'Yes'
                    body = render_to_string(
                        'checkout/confirmation_emails/farmer_email_body_delivery.txt',
                    )
                else:
                    body_context['delivery'] = 'Yes'
                    body = render_to_string(
                        'checkout/confirmation_emails/farmer_email_body.txt',
                    )

                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient]
                )

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email

        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        order_number = intent.metadata.order_number
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    order_number=order_number
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            order.wh_success = True
            order.save()
            self._send_confirmation_email(order)
            self._send_farmer_email(order)
            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Verified order already in database'),
                status=200)
        else:
            order = None
            try:
                address = Address.objects.create(
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    town_or_city=shipping_details.address.city,
                    county=shipping_details.address.state,
                    postcode=shipping_details.address.postal_code,
                    country=shipping_details.address.country,
                )
                order = Order.objects.create(
                    first_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    address=address,
                    stripe_pid=pid,
                )
                for product_id, quantity in json.loads(cart).items():
                    product = ProductVariant.objects.get(pk=product_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    farmer_order, created = (
                        FarmerOrder.objects.update_or_create(
                            order=order,
                        ))
                    farmer_order.farmer = (
                        order_line_item.product.product.created_by
                    )
                    order_line_item.farmer_order = farmer_order
                    order_line_item.save()
                    farmer_order.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        order.wh_success = True
        order.save()
        self._send_confirmation_email(order)
        return HttpResponse(
            content=(f'Webhook received: {event["type"]} | SUCCESS: '
                     'Created order in webhook'),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
