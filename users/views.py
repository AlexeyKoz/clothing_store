from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import ShippingAddress
from orders.forms import ShippingAddressForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from allauth.account.views import EmailView


@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')


@login_required
def edit_address(request):
    try:
        address = request.user.shippingaddress
    except ShippingAddress.DoesNotExist:
        address = ShippingAddress(user=request.user)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('orders:checkout_address')
    else:
        form = ShippingAddressForm(instance=address)

    return render(request, 'users/edit_address.html', {'form': form})


@login_required
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been successfully logged out.")
        return redirect('home')
    return redirect('home')


@login_required
def email_change_view(request):
    return EmailView.as_view()(request)
