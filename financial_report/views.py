from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from io import BytesIO
from goals.models import FinancialGoal
from income.models import Income
from expenses.models import Expense
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from datetime import datetime
import json
from .utils import compare_reports


@login_required
def financial_report(request):
    income_data = Income.objects.filter(user=request.user)
    
    income_by_type = [
        {'income_type': income_type, 'amount': sum(income.amount for income in income_data.filter(income_type=income_type))}
        for income_type, _ in Income.INCOME_TYPES
    ]

    expenses_data = Expense.objects.filter(user=request.user)
    expenses_by_category = [
        {'category': expense.category, 'amount': expense.amount} for expense in expenses_data
    ]
    
    goals_data = FinancialGoal.objects.filter(user=request.user)
    goals_by_category = [
        {'category': goal.category, 'name': goal.name, 'target_amount': goal.target_amount, 'current_amount': goal.current_amount, 'target_date': goal.target_date, 'progress': goal.progress_percentage()}
        for goal in goals_data
    ]

    income_labels = [income['income_type'] for income in income_by_type]
    income_values = [income['amount'] for income in income_by_type]
    
    fig, ax = plt.subplots()
    ax.bar(income_labels, income_values, color='blue')
    ax.set_title('Доходи по типах')
    ax.set_xlabel('Тип доходу')
    ax.set_ylabel('Сума')

    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    income_chart = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    expense_labels = [expense['category'] for expense in expenses_by_category]
    expense_values = [expense['amount'] for expense in expenses_by_category]
    
    fig, ax = plt.subplots()
    ax.bar(expense_labels, expense_values, color='green')
    ax.set_title('Витрати по категоріях')
    ax.set_xlabel('Категорія витрат')
    ax.set_ylabel('Сума')

    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    expense_chart = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    goal_labels = [goal['name'] for goal in goals_by_category]
    goal_progress = [goal['progress'] for goal in goals_by_category]
    
    fig, ax = plt.subplots()
    ax.bar(goal_labels, goal_progress, color='purple')
    ax.set_title('Прогрес фінансових цілей')
    ax.set_xlabel('Назва цілі')
    ax.set_ylabel('Прогрес (%)')

    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    goal_chart = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    return render(request, 'reports/financial_report.html', {
        'income': {'total_income': sum(income.amount for income in income_data), 'by_type': income_by_type},
        'expenses': {'total_expense': sum(expense['amount'] for expense in expenses_by_category), 'by_category': expenses_by_category},
        'goals': goals_by_category, 
        'income_chart': income_chart,
        'expense_chart': expense_chart,
        'goal_chart': goal_chart, 
    })


@login_required
def compare_report(request):
    if request.method == 'GET':
        start_date_1_str = request.GET.get('start_date_1')
        end_date_1_str = request.GET.get('end_date_1')
        start_date_2_str = request.GET.get('start_date_2')
        end_date_2_str = request.GET.get('end_date_2')

        if start_date_1_str and end_date_1_str and start_date_2_str and end_date_2_str:
            try:
                start_date_1 = datetime.strptime(start_date_1_str, '%d.%m.%Y')
                end_date_1 = datetime.strptime(end_date_1_str, '%d.%m.%Y')
                start_date_2 = datetime.strptime(start_date_2_str, '%d.%m.%Y')
                end_date_2 = datetime.strptime(end_date_2_str, '%d.%m.%Y')

                data = compare_reports(request.user, start_date_1, end_date_1, start_date_2, end_date_2)

                data['start_date_1'] = start_date_1.strftime('%d.%m.%Y')
                data['end_date_1'] = end_date_1.strftime('%d.%m.%Y')
                data['start_date_2'] = start_date_2.strftime('%d.%m.%Y')
                data['end_date_2'] = end_date_2.strftime('%d.%m.%Y')

                data['period1_label'] = f"{data['start_date_1']} - {data['end_date_1']}"
                data['period2_label'] = f"{data['start_date_2']} - {data['end_date_2']}"
                data['period1_report_json'] = json.dumps(data['period1']['report'])
                data['period2_report_json'] = json.dumps(data['period2']['report'])

                return render(request, "reports/compare.html", data)
            except ValueError:
                return render(request, "reports/compare.html", {'error': 'Будь ласка, введіть дати у форматі дд.мм.рррр.'})
        else:
            return render(request, "reports/compare.html", {'error': 'Будь ласка, виберіть два періоди для порівняння.'})

    return render(request, "reports/compare.html")


