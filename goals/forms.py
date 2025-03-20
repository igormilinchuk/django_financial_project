from django import forms
from .models import FinancialGoal, GoalContribution

class FinancialGoalForm(forms.ModelForm):
    RECURRENCE_CHOICES = [
        ('monthly', 'Щомісячний'),
        ('weekly', 'Щотижневий'),
        ('daily', 'Щоденний'),
    ]
    recurrence = forms.ChoiceField(choices=RECURRENCE_CHOICES, required=False)
    
    target_date = forms.DateField(
        widget=forms.TextInput(attrs={"class": "flatpickr"})
    )

    class Meta:
        model = FinancialGoal
        fields = ['name', 'target_amount', 'target_date']

class GoalContributionForm(forms.ModelForm):
    class Meta:
        model = GoalContribution
        fields = ['amount']
