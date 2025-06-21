from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from cart.models import CartItem
from .models import Order, OrderItem
from orders.models import ShippingAddress


@login_required
def order_summary(request):
    if not request.session.get("terms_accepted"):
        return redirect("orders:checkout_payment")

    # Удаляем старые незавершённые заказы, чтобы не мешали
    Order.objects.filter(user=request.user, status="pending").delete()

    try:
        shipping_address = request.user.shippingaddress
    except ShippingAddress.DoesNotExist:
        messages.error(request, "Shipping address is missing.")
        return redirect('orders:checkout_address')

    payment_method = request.session.get("payment_method", "")
    installments = request.session.get("installments", 1)
    name_on_bill = request.session.get("checkout_name", "")

    order = Order.objects.create(
        user=request.user,
        shipping_address=shipping_address,
        payment_method=payment_method,
        installments=installments,
        name_on_bill=name_on_bill,
        full_name=shipping_address.full_name,
        address=shipping_address.address,
        email=request.user.email,
        phone="N/A",
    )

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )
    cart_items.delete()

    return render(request, "orders/order_summary.html", {
        "order": order
    })


@login_required
def finalize_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    if request.method == "POST":
        order.status = "confirmed"
        order.save()
        messages.success(request, "Order finalized successfully!")
        return redirect("orders:order_detail", order_id=order.id)
    return redirect("orders:order_summary")


@login_required
def generate_invoice(request, order_id):
    order = Order.objects.get(pk=order_id, user=request.user)
    template = get_template("orders/invoice.html")
    html = template.render({'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation error', status=500)
    return response


@login_required
def order_detail(request, order_id):
    try:
        if request.user.is_staff:
            order = Order.objects.get(id=order_id)
        else:
            order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, "The requested order could not be found.")
        return redirect('orders:order_list')

    support_tickets = order.support_tickets.all().order_by('-created_at')

    # Pre-process items to avoid template logic errors
    items_for_template = []
    for item in order.items.all():
        items_for_template.append({
            'image_url': item.product.image.url if item.product.image else '/static/placeholder.png',
            'product_name': item.product.name,
            'get_absolute_url': item.product.get_absolute_url() if hasattr(item.product, 'get_absolute_url') else '#',
            'quantity': item.quantity,
            'total_price': item.total_price,
        })

    context = {
        "order": order,
        "support_tickets": support_tickets,
        "order_items": items_for_template,
    }
    return render(request, "orders/order_detail.html", context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def checkout_address(request):
    try:
        address = request.user.shippingaddress
    except ShippingAddress.DoesNotExist:
        messages.warning(
            request, "Please fill your shipping address in your profile.")
        return redirect("users:edit_address")

    if request.method == "POST":
        request.session["checkout_name"] = request.POST.get("billing_name", "")
        return redirect("orders:checkout_payment")

    return render(request, "orders/checkout_address.html", {
        "address": address,
    })


@login_required
def checkout_payment(request):
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        installments = request.POST.get("installments")
        terms_accepted = request.POST.get("confirm")

        if not (payment_method and installments and terms_accepted):
            messages.error(
                request, "Please fill in all fields and confirm the terms.")
            return render(request, "orders/checkout_payment.html")

        request.session["payment_method"] = payment_method
        request.session["installments"] = installments
        request.session["terms_accepted"] = terms_accepted == "on"

        return redirect("orders:order_summary")

    return render(request, "orders/checkout_payment.html")
