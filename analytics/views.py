from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
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
        total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expenses

        data = {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance
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
        first_day_current = today.replace(day=1)
        first_day_last_month = (first_day_current - timedelta(days=1)).replace(day=1)

        incomes_current = Income.objects.filter(user=user, date__range=[first_day_current, today]).aggregate(Sum('amount'))['amount__sum'] or 0
        expenses_current = Expense.objects.filter(user=user, date__range=[first_day_current, today]).aggregate(Sum('amount'))['amount__sum'] or 0
        incomes_previous = Income.objects.filter(user=user, date__range=[first_day_last_month, first_day_current - timedelta(days=1)]).aggregate(Sum('amount'))['amount__sum'] or 0
        expenses_previous = Expense.objects.filter(user=user, date__range=[first_day_last_month, first_day_current - timedelta(days=1)]).aggregate(Sum('amount'))['amount__sum'] or 0

        data = {
            "current_month": {
                "income": incomes_current,
                "expenses": expenses_current
            },
            "last_month": {
                "income": incomes_previous,
                "expenses": expenses_previous
            }
        }

    elif report_type == "category_expenses":
        category_expenses = Expense.objects.filter(user=user).values('category').annotate(total=Sum('amount'))
        data = {
            "categories": [
                {"category": expense['category'], "total": expense['total']} for expense in category_expenses
            ]
        }

    report = Report.objects.create(user=user, report_type=report_type, data=json.dumps(data))

    return render(request, "analytics/report_detail.html", {"report": report})
