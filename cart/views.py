from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalog.models import Product
from .models import CartItem
from django.contrib import messages

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("cart:view_cart")

@login_required
def view_cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    return render(request, "cart/view_cart.html", {"items": items, "total": total})



@login_required
def remove_from_cart(request, product_id):
    item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect("cart:view_cart")
