from django.db import models
from users.models import User
from django.utils.timezone import now
from datetime import date
from expenses.models import Expense

class FinancialGoal(models.Model):
    GOAL_TYPE_CHOICES = [
        ('saving', 'Накопичення'),
        ('spending', 'Зменшення витрат'),
        ('investment', 'Інвестування'),
    ]

    CATEGORY_CHOICES = [
        ('travel', 'Подорожі'),
        ('housing', 'Житло'),
        ('education', 'Освіта'),
        ('retirement', 'Пенсія'),
        ('emergency', 'Резервний фонд'),
        ('other', 'Інше'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    name = models.CharField(max_length=255)
    goal_type = models.CharField(max_length=12, choices=GOAL_TYPE_CHOICES)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='other')
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['target_date']

    def progress_percentage(self):
        return min(100, round((self.current_amount / self.target_amount) * 100, 2)) if self.target_amount > 0 else 0

    def is_goal_achieved(self):
        return self.current_amount >= self.target_amount

    def __str__(self):
        return f"{self.name} ({self.get_goal_type_display()} - {self.progress_percentage()}%)"


class GoalContribution(models.Model):
    goal = models.ForeignKey(FinancialGoal, on_delete=models.CASCADE, related_name="contributions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.goal.current_amount += self.amount
        self.goal.save()

        Expense.objects.create(
            user=self.goal.user,
            amount=self.amount,
            category="goals", 
            description=f"Внесок у ціль: {self.goal.name}"
        )

    def __str__(self):
        return f"{self.goal.name}: +{self.amount} грн ({self.date})"
