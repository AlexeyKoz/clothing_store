from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from cart.models import CartItem
from .models import Order, OrderItem
from .forms import OrderForm

@login_required
def order_summary(request):
    if not request.session.get("terms_accepted"):
        return redirect("orders:checkout_payment")

    order = Order.objects.filter(user=request.user).last()
    return render(request, "orders/order_detail.html", {
        "order": order,
        "name_on_bill": request.session.get("checkout_name", ""),
        "payment_method": request.session.get("payment_method", ""),
        "installments": request.session.get("installments", "1"),
    })


@login_required
def create_order(request):
    cart_items = CartItem.objects.filter(user=request.user)

    # Если корзина пуста — редирект обратно
    if not cart_items.exists():
        return redirect('cart:checkout')

    # Создаём заказ
    order = Order.objects.create(user=request.user)

    # Добавляем позиции в заказ
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    # Очищаем корзину после успешного создания
    cart_items.delete()

    # Редирект на страницу заказа
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})



@login_required
def checkout_address(request):
    try:
        address = request.user.shippingaddress
    except ShippingAddress.DoesNotExist:
        messages.warning(request, "Please fill your shipping address in your profile.")
        return redirect("profile:edit_address")

    if request.method == "POST":
        request.session["checkout_name"] = request.POST.get("billing_name", "")
        return redirect("orders:checkout_payment")

    return render(request, "orders/checkout_address.html", {
        "address": address,
    })

# orders/views.py
@login_required
def checkout_payment(request):
    if request.method == "POST":
        # Сохраняем в сессию
        request.session["payment_method"] = request.POST.get("payment_method")
        request.session["installments"] = request.POST.get("installments")
        request.session["terms_accepted"] = True
        return redirect("orders:order_summary")
    return render(request, "orders/checkout_payment.html")


