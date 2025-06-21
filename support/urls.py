from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('order/<int:order_id>/ticket/new/',
         views.create_ticket, name='create_ticket'),
    path('admin/tickets/', views.admin_ticket_list, name='admin_ticket_list'),
    path('admin/tickets/<int:ticket_id>/',
         views.ticket_detail, name='ticket_detail'),
    path('admin/tickets/<int:ticket_id>/delete/',
         views.delete_ticket, name='delete_ticket'),
]
