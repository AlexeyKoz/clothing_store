from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import ShippingAddress
from orders.forms import ShippingAddressForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from allauth.account.views import EmailView
from django.http import HttpResponseRedirect
from allauth.account.models import EmailAddress
from .forms import ChangeEmailForm, ChangeNameForm


@login_required
def dashboard_view(request):
    """
    Displays the user's account settings dashboard, including their
    shipping address information if it exists.
    """
    try:
        shipping_address = request.user.shippingaddress
    except ShippingAddress.DoesNotExist:
        shipping_address = None

    context = {
        'shipping_address': shipping_address
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def edit_address(request):
    """
    Handles fetching and updating the user's shipping address.
    Uses get_or_create to ensure an address instance always exists
    before rendering or processing the form.
    """
    # Use get_or_create. It returns the object and a boolean `created`.
    address, created = ShippingAddress.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.get_full_name()
                  or request.user.username}
    )

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            # The full_name is now set on creation and not edited.
            # We just save the form which contains the other address fields.
            form.save()
            messages.success(
                request, "Your shipping address has been updated successfully!")
            # Redirect to dashboard after save
            return redirect('users:dashboard')
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
def manage_email_view(request):
    """
    Handles the entire email change process, including superuser restrictions,
    displaying the current and pending emails, and processing the change form.
    """
    if request.user.is_superuser:
        messages.warning(
            request, "Superuser email must be changed from the admin panel for security reasons.")
        return render(request, 'account/email.html', {'superuser_restriction': True})

    pending_email = EmailAddress.objects.filter(
        user=request.user, verified=False).first()

    if request.method == "POST":
        # Logic for the "Resend Verification" button
        if 'action_send' in request.POST and pending_email:
            pending_email.send_confirmation(request)
            messages.success(
                request, f"A new verification link has been sent to {pending_email.email}.")
            return redirect('users:email_change')

        # Logic for the "Change Email" form
        form = ChangeEmailForm(request.POST, user=request.user)
        if form.is_valid():
            # If a different pending email exists, remove it.
            if pending_email:
                pending_email.delete()

            new_email = form.cleaned_data['email']
            EmailAddress.objects.add_email(
                request, request.user, new_email, confirm=True)
            messages.info(
                request, f"A verification link has been sent to {new_email}. Please check your inbox to finalize the change.")
            return redirect('users:email_change')
    else:
        form = ChangeEmailForm()

    context = {
        'form': form,
        'pending_email': pending_email,
        'current_email': EmailAddress.objects.get_primary(request.user),
    }
    return render(request, 'account/email.html', context)


@login_required
def change_name_view(request):
    """
    Allows a regular user to change their first and last name.
    Superusers are blocked and redirected.
    """
    if request.user.is_superuser:
        messages.error(
            request, "Superuser names cannot be changed from this page.")
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = ChangeNameForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save(update_fields=['first_name', 'last_name'])
            messages.success(
                request, "Your name has been updated successfully!")
            return redirect('users:dashboard')
    else:
        form = ChangeNameForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        })

    return render(request, 'users/change_name.html', {'form': form})
