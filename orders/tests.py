from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from catalog.models import Category, Brand, Product
from cart.models import CartItem
from .models import ShippingAddress, Order, OrderItem


class OrderSummaryViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test", slug="test")
        self.brand = Brand.objects.create(name="Brand")
        self.user = User.objects.create_user(username="user", password="pass")
        self.product = Product.objects.create(
            name="Item",
            description="Desc",
            price=10,
            category=self.category,
            brand=self.brand,
        )
        self.url = reverse("orders:order_summary")
        self.checkout_payment_url = reverse("orders:checkout_payment")
        self.checkout_address_url = reverse("orders:checkout_address")

    def _login(self):
        self.client.force_login(self.user)

    def test_requires_login(self):
        response = self.client.get(self.url)
        login_url = reverse("account_login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")

    def test_redirect_without_terms(self):
        self._login()
        response = self.client.get(self.url)
        self.assertRedirects(response, self.checkout_payment_url)

    def test_redirect_without_address(self):
        self._login()
        session = self.client.session
        session["terms_accepted"] = True
        session.save()

        response = self.client.get(self.url)

        # Проверяем, что происходит редирект
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.checkout_address_url)

    def test_creates_order_and_items(self):
        self._login()
        ShippingAddress.objects.create(
            user=self.user,
            full_name="John Doe",
            address="Main St",
            city="City",
            zip_code="12345",
            country="AA",
        )
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)

        session = self.client.session
        session["terms_accepted"] = True
        session.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/order_summary.html")

        order = Order.objects.get()
        self.assertEqual(order.user, self.user)
        self.assertEqual(OrderItem.objects.count(), 1)
        item = OrderItem.objects.get()
        self.assertEqual(item.quantity, 2)
        self.assertEqual(CartItem.objects.count(), 0)