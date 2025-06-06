from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Category, Brand, Product
from .models import CartItem

# Create your tests here.

class AddToCartViewTests(TestCase):
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
        self.url = reverse("cart:add_to_cart", args=[self.product.id])
        self.cart_url = reverse("cart:view_cart")

    def test_add_requires_login(self):
        response = self.client.post(self.url)
        login_url = reverse("account_login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")
        self.assertEqual(CartItem.objects.count(), 0)

    def test_add_creates_item(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, self.cart_url)
        item = CartItem.objects.get()
        self.assertEqual(item.user, self.user)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 1)

    def test_add_increases_quantity(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, self.cart_url)
        item = CartItem.objects.get()
        self.assertEqual(item.quantity, 2)