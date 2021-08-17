from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib import messages
from products.models import ProductVariant


class Cart(TemplateView):
    """ View to display the cart """
    template_name = "cart/cart.html"


def add_to_cart(request):
    """ Add a quantity of the specified product to the shopping cart """
    product_id = request.POST.get('product_id')
    product = get_object_or_404(ProductVariant, pk=product_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
        messages.success(request, (
            f'Added {quantity} {product} to cart.'
        ))
    else:
        cart[product_id] = quantity
        messages.success(request, (
            f'Added {quantity} {product} to cart.'
        ))

    redirect_url = request.POST.get('redirect_url')
    request.session['cart'] = cart
    return redirect(redirect_url)


def update_cart(request):
    """ Update the quantities of cart items """

    cart = request.session.get('cart', {})
    print(request.POST)
    for item in request.POST:
        if 'csrf' in item:
            # ignore csrf token
            pass
        elif 'item-delete' in item:
            if request.POST[item] == '1':
                # if value of hidden input is 1, delete the item
                id = item.replace('item-delete-', '')
                cart.pop(id, None)
        else:
            # update the cart item quantity from the form input
            cart[item] = int(request.POST[item])
    messages.success(request, ('Cart updated.'))
    request.session['cart'] = cart
    return redirect(reverse('cart'))
