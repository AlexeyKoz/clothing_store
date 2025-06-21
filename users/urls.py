from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path("edit-address/", views.edit_address, name="edit_address"),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('email/', views.manage_email_view, name='email_change'),
    path('change-name/', views.change_name_view, name='change_name'),
]
