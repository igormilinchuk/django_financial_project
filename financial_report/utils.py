from datetime import date
from django.db.models import Sum, Count, Q
from goals.models import FinancialGoal
from income.models import Income
from expenses.models import Expense
from django.db import models
import decimal

def get_date_range_filter(start_date, end_date):
    return Q(date__gte=start_date) & Q(date__lte=end_date)

def generate_goals_report(user, start_date: date, end_date: date):
    goals = FinancialGoal.objects.filter(user=user, created_at__range=(start_date, end_date))
    
    achieved = goals.filter(current_amount__gte=models.F('target_amount')).count()
    in_progress = goals.filter(current_amount__lt=models.F('target_amount')).count()
    total = achieved + in_progress

    achieved_percent = (achieved / total * 100) if total else 0
    in_progress_percent = (in_progress / total * 100) if total else 0

    return {
        "achieved": achieved,
        "in_progress": in_progress,
        "achieved_percent": round(achieved_percent, 2),
        "in_progress_percent": round(in_progress_percent, 2),
    }

def generate_income_report(user, start_date: date, end_date: date):
    incomes = Income.objects.filter(user=user, date__range=(start_date, end_date))
    total = incomes.aggregate(total_amount=Sum("amount"))["total_amount"] or 0

    by_type = incomes.values("income_type").annotate(amount=Sum("amount"))

    return {
        "total_income": total,
        "by_type": list(by_type),
    }

def generate_expense_report(user, start_date: date, end_date: date):
    expenses = Expense.objects.filter(user=user, date__range=(start_date, end_date))
    total = expenses.aggregate(total_amount=Sum("amount"))["total_amount"] or 0

    by_category = expenses.values("category").annotate(amount=Sum("amount"))

    return {
        "total_expense": total,
        "by_category": list(by_category),
    }

def generate_full_report(user, start_date: date, end_date: date):
    return {
        "goals": generate_goals_report(user, start_date, end_date),
        "income": generate_income_report(user, start_date, end_date),
        "expenses": generate_expense_report(user, start_date, end_date),
    }

def compare_reports(user, start1, end1, start2, end2):
    report1 = generate_full_report(user, start1, end1)
    report2 = generate_full_report(user, start2, end2)

    def diff(val1, val2):
        return round(val1 - val2, 2)

    def convert_decimal_to_float(data):
        # Перевести Decimal в float рекурсивно, якщо в словнику є Decimal
        if isinstance(data, decimal.Decimal):
            return float(data)
        elif isinstance(data, dict):
            return {key: convert_decimal_to_float(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [convert_decimal_to_float(item) for item in data]
        else:
            return data

    report1 = convert_decimal_to_float(report1)
    report2 = convert_decimal_to_float(report2)

    return {
        "period1": {
            "start": start1,
            "end": end1,
            "report": report1,
        },
        "period2": {
            "start": start2,
            "end": end2,
            "report": report2,
        },
        "difference": {
            "income": diff(report1["income"]["total_income"], report2["income"]["total_income"]),
            "expense": diff(report1["expenses"]["total_expense"], report2["expenses"]["total_expense"]),
            "goals_achieved": diff(report1["goals"]["achieved"], report2["goals"]["achieved"]),
        }
    }
