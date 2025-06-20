from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CartItemViewSet, OrderViewSet, UserViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart-items', CartItemViewSet, basename='cart-item')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 