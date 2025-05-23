from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPES = [
        ('regular', 'Regular'),
        ('vip', 'VIP'),
        ('intl', 'International'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='regular')
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
from django.db import models

# Create your models here.
