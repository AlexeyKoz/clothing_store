from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalog.models import Product
from .models import CartItem
from django.contrib import messages
from decimal import Decimal
from django.views.decorators.http import require_POST

@require_POST
@login_required
def update_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, user=request.user, product=product)

    action = request.POST.get("action")
    if action == "increase":
        cart_item.quantity += 1
        cart_item.save()
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect("cart:view_cart")


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
    items = CartItem.objects.filter(user=request.user).order_by('id')
    total = sum(item.total_price() for item in items)
    return render(request, "cart/view_cart.html", {"items": items, "total": total})



@login_required
def remove_from_cart(request, product_id):
    item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect("cart:view_cart")


@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.total_price() for item in items)
    tax_rate = Decimal("0.18")  # taxes at 18%
    tax = (subtotal * tax_rate).quantize(Decimal("0.01"))
    total = (subtotal + tax).quantize(Decimal("0.01"))

    return render(request, "cart/checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "tax": tax,
        "total": total
    })

