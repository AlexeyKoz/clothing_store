from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path("edit-address/", views.edit_address, name="edit_address"),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('email/', views.email_change_view, name='email_change'),
]
