from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    REPORT_TYPES = [
        ('income_expense', 'Доходи та витрати'),
        ('goal_progress', 'Прогрес цілей'),
        ('comparison', 'Порівняння періодів'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField() 

    def __str__(self):
        return f"{self.get_report_type_display()} ({self.created_at.date()})"
