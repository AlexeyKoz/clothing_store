from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Добавлено для отслеживания изменений

    class Meta:
        unique_together = ('user', 'product')  # Гарантирует один отзыв на пользователя/товар
        ordering = ['-created_at']  # Сортировка по умолчанию

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"