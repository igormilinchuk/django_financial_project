from django.db import models
from users.models import User 

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Їжа'),
        ('transport', 'Транспорт'),
        ('housing', 'Житло'),
        ('entertainment', 'Розваги'),
        ('clothing', 'Одяг'),
        ('health', 'Здоров\'я'),
        ('insurance', 'Страхування'),
        ('utilities', 'Комунальні послуги'),
        ('emergency', 'Резервний фонд'),
        ('goals', 'Цілі'),
        ('other', 'Інше'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount} грн"
