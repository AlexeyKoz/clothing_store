from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path("", views.order_list, name="order_list"),
    path("order/summary/", views.order_summary, name="order_summary"),
    path("checkout/address/", views.checkout_address, name="checkout_address"),
    path("checkout/payment/", views.checkout_payment, name="checkout_payment"),
]
