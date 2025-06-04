from django.contrib.auth.models import User
from django.db import models


class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.full_name}, {self.address}, {self.city}, {self.country}"


class UserProfile(models.Model):
    USER_TYPES = [
        ('regular', 'Regular'),
        ('vip', 'VIP'),
        ('intl', 'International'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='regular')
    address = models.TextField(blank=True)
    country = models.CharField(max_length=2, default='IL')
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.user_type})"

    def get_country_display(self):
        return self.country
