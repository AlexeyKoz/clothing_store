from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Category, Brand, Product, ProductLike


class LikeProductViewTests(TestCase):
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
        self.url = reverse("catalog:like_product", args=[self.product.id])
        self.detail_url = reverse("catalog:product_detail", args=[self.product.id])

    def test_like_requires_login(self):
        response = self.client.post(self.url)
        login_url = reverse("account_login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")
        self.assertEqual(ProductLike.objects.count(), 0)

    def test_create_like(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, HTTP_REFERER=self.detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ProductLike.objects.filter(user=self.user, product=self.product).exists()
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("I like it !", messages)

    def test_delete_like(self):
        ProductLike.objects.create(user=self.user, product=self.product)
        self.client.force_login(self.user)
        response = self.client.post(self.url, HTTP_REFERER=self.detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            ProductLike.objects.filter(user=self.user, product=self.product).exists()
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Like Deleted.", messages)