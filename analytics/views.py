from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Report
from income.models import Income
from expenses.models import Expense
from goals.models import FinancialGoal
from datetime import datetime, timedelta
import json

@login_required
def generate_report(request, report_type):
    user = request.user
    data = {}

    if report_type == "income_expense":
        incomes = Income.objects.filter(user=user)
        expenses = Expense.objects.filter(user=user)
        data = {
            "total_income": sum(i.amount for i in incomes),
            "total_expenses": sum(e.amount for e in expenses),
            "balance": sum(i.amount for i in incomes) - sum(e.amount for e in expenses)
        }

    elif report_type == "goal_progress":
        goals = FinancialGoal.objects.filter(user=user)
        data = {
            "goals": [
                {
                    "name": goal.name,
                    "target": goal.target_amount,
                    "current": goal.current_amount,
                    "progress": goal.progress_percentage
                } for goal in goals
            ]
        }

    elif report_type == "comparison":
        today = datetime.today()
        last_month = today - timedelta(days=30)

        incomes_current = Income.objects.filter(user=user, date__month=today.month)
        expenses_current = Expense.objects.filter(user=user, date__month=today.month)
        incomes_previous = Income.objects.filter(user=user, date__month=last_month.month)
        expenses_previous = Expense.objects.filter(user=user, date__month=last_month.month)

        data = {
            "current_month": {
                "income": sum(i.amount for i in incomes_current),
                "expenses": sum(e.amount for e in expenses_current)
            },
            "last_month": {
                "income": sum(i.amount for i in incomes_previous),
                "expenses": sum(e.amount for e in expenses_previous)
            }
        }

    report = Report.objects.create(user=user, report_type=report_type, data=data)

    return render(request, "reports/report_detail.html", {"report": report})
