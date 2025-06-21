from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SupportTicketForm
from .models import SupportTicket
from orders.models import Order
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.


@login_required
def create_ticket(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.order = order
            ticket.save()
            messages.success(
                request, "Your support request has been successfully submitted. Our team will review your inquiry and respond via email. You can view the status of your ticket on the order detail page.")
            return redirect('orders:order_detail', order_id=order.id)
    else:
        form = SupportTicketForm()

    context = {
        'form': form,
        'order': order
    }
    return render(request, 'support/create_ticket.html', context)


@staff_member_required
def admin_ticket_list(request):
    sort_by = request.GET.get('sort', 'created_at')
    if sort_by not in ['status', 'created_at', 'user__username']:
        sort_by = 'created_at'

    tickets = SupportTicket.objects.all().order_by(sort_by)
    context = {'tickets': tickets}
    return render(request, 'support/admin_ticket_list.html', context)


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    if not request.user.is_staff:
        messages.error(
            request, "You do not have permission to perform this action.")
        return redirect('home')  # Or wherever you want to redirect non-staff

    if request.method == "POST":
        ticket.delete()
        messages.success(request, f"Ticket #{ticket.id} has been deleted.")
        return redirect('support:admin_ticket_list')

    # If it's a GET request, you could render a confirmation page
    # For simplicity, we'll just redirect.
    return redirect('support:admin_ticket_list')


@staff_member_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)

    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in SupportTicket.STATUS_CHOICES]:
            ticket.status = new_status
            ticket.save()
            messages.success(
                request, f"Ticket #{ticket.id} status updated to '{ticket.get_status_display()}'.")
            return redirect('support:admin_ticket_list')

    # Prepare status choices for the template to avoid logic errors
    status_choices = []
    for value, name in SupportTicket.STATUS_CHOICES:
        status_choices.append({
            'value': value,
            'name': name,
            'is_selected': ticket.status == value
        })

    context = {
        'ticket': ticket,
        'status_choices': status_choices,
        'order_number': ticket.order.order_number,
        'order_id': ticket.order.id,
    }
    return render(request, 'support/ticket_detail_new.html', context)
