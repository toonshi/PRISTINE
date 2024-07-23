
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from item.models import Item  # Import Item from the shop app
from .models import cartItem, Cart, order

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = cartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    cart_item_count = cartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_item_count': cart_item_count})

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cartItem.objects.filter(cart=cart)

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'cart': cart
    })

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(Item, id=item_id)
    cart_item = get_object_or_404(cartItem, cart=cart, item=item)
    cart_item.delete()

    return redirect('cart:cart_detail')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cartItem.objects.filter(cart=cart)

    if request.method == 'POST':
        new_order = order(user=request.user, total_price=calculate_total_price(cart_items))
        new_order.save()
        new_order.items.set(cart_items)
        new_order.save()

        cart_items.delete()
        return redirect('shop:order_confirmation', order_id=new_order.id)

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'cart': cart
    })

def calculate_total_price(cart_items):
    total_price = 0
    for item in cart_items:
        total_price += item.quantity * item.item.price
    return total_price
