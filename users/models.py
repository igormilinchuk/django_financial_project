from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    currency = models.CharField(max_length=10, default="USD")  # Валюта користувача
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Середній дохід

    def __str__(self):
        return self.username


class FinancialGoal(models.Model):
    GOAL_TYPES = [
        ('saving', 'Накопичення'),
        ('expense_reduction', 'Зменшення витрат'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="financial_goals") 
    name = models.CharField(max_length=255)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    current_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def progress_percentage(self):
        return (self.current_savings / self.target_amount) * 100 if self.target_amount else 0

    def __str__(self):
        return f"{self.name} - {self.target_amount} {self.user.currency}"
