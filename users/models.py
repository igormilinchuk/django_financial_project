from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    currency = models.CharField(max_length=10, default="USD")  # Валюта користувача
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Середній дохід

    def __str__(self):
        return self.username


