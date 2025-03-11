from django.db import models
from users.models import User
from django.utils.timezone import now
from datetime import date

class FinancialGoal(models.Model):
    GOAL_TYPE_CHOICES = [
        ('saving', 'Накопичення'),
        ('spending', 'Зменшення витрат'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    name = models.CharField(max_length=255)
    goal_type = models.CharField(max_length=10, choices=GOAL_TYPE_CHOICES)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def remaining_amount(self):
        return self.target_amount - self.current_amount

    def months_remaining(self):
        today = date.today()
        return max(1, (self.target_date.year - today.year) * 12 + (self.target_date.month - today.month))

    def monthly_contribution(self):
        if self.goal_type == "saving":
            return self.remaining_amount() / self.months_remaining()
        return None  # Для витрат не потрібен розрахунок

    def progress_percentage(self):
        return min(100, (self.current_amount / self.target_amount) * 100)

    def __str__(self):
        return f"{self.name} ({self.get_goal_type_display()})"
