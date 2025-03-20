from django.db import models
from users.models import User  
from django.utils.timezone import now

class Income(models.Model):
    INCOME_TYPES = [
        ('salary', 'Заробітна плата'),
        ('investment', 'Інвестиції'),
        ('freelance', 'Фріланс'),
        ('other', 'Інше'),
    ]

    RECURRENCE_CHOICES = [
        ('one-time', 'Разовий'),
        ('monthly', 'Щомісячний'),
        ('weekly', 'Щотижневий'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incomes")
    source = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    income_type = models.CharField(max_length=20, choices=INCOME_TYPES, default='other')
    date = models.DateField(default=now)
    recurrence = models.CharField(max_length=20, choices=RECURRENCE_CHOICES, default='one-time')

    def __str__(self):
        return f"{self.source} - {self.amount} {self.user.currency}"
