from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("view/", views.view_cart, name="view_cart"),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path("update/<int:product_id>/", views.update_quantity, name="update_quantity"),

]
