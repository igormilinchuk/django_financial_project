from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from .models import Report
from income.models import Income
from expenses.models import Expense
from goals.models import FinancialGoal
from datetime import datetime, timedelta, date
from reportlab.pdfgen import canvas
import json
import decimal

# Function to convert date objects to strings
def convert_dates_to_string(obj):
    if isinstance(obj, date):
        return obj.isoformat()  # Convert date to 'YYYY-MM-DD' string
    elif isinstance(obj, dict):
        return {key: convert_dates_to_string(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates_to_string(item) for item in obj]
    else:
        return obj

# Function to convert decimal.Decimal to float for serialization
def decimal_to_float(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: decimal_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(item) for item in obj]
    else:
        return obj

# Get income report
def get_income_report(user, start_date, end_date):
    income_data = Income.objects.filter(user=user, date__range=[start_date, end_date])
    total_income = income_data.aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = float(total_income)
    return {"total_income": total_income, "income_records": list(income_data.values())}

# Get expense report
def get_expense_report(user, start_date, end_date, category=None):
    expenses = Expense.objects.filter(user=user, date__range=[start_date, end_date])
    if category:
        expenses = expenses.filter(category=category)
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = float(total_expenses)
    return {"total_expenses": total_expenses, "expense_records": list(expenses.values())}

# Get goals report
def get_goals_report(user):
    goals = FinancialGoal.objects.filter(user=user)
    goal_data = [{
        "name": goal.name,
        "target_amount": float(goal.target_amount),
        "current_amount": float(goal.current_amount),
        "progress": (float(goal.current_amount) / float(goal.target_amount) * 100) if goal.target_amount > 0 else 0
    } for goal in goals]
    return {"goals": goal_data}

# Report dashboard view
@login_required
def report_dashboard(request):
    return render(request, 'analytics/report_dashboard.html')

# Generate the report and save it
def generate_report(request):
    report_type = request.GET.get('type')
    start_date = request.GET.get('start_date', (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', datetime.today().strftime('%Y-%m-%d'))
    category = request.GET.get('category', None)
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    user = request.user
    data = {}

    # Generate the appropriate report based on the type
    if report_type == "income":
        data = get_income_report(user, start_date, end_date)
    elif report_type == "expense":
        data = get_expense_report(user, start_date, end_date, category)
    elif report_type == "goals":
        data = get_goals_report(user)

    # Convert decimal values to float and date objects to string
    data = decimal_to_float(data)
    data = convert_dates_to_string(data)
    
    # Create the report object and store it in the database
    report = Report.objects.create(user=user, report_type=report_type, data=json.dumps(data))
    
    return render(request, 'analytics/report_detail.html', {"report": report, "data": data})

# Export report to PDF
@login_required
def export_report_pdf(request, report_id):
    try:
        # Fetch the report by its ID and user
        report = Report.objects.get(id=report_id, user=request.user)
        report_data = json.loads(report.data)
    except Report.DoesNotExist:
        return HttpResponse("Report not found", status=404)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{report_id}.pdf"'
    
    # Create PDF content
    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Report Type: {report.report_type}")
    p.drawString(100, 780, "Data:")
    y = 760
    for key, value in report_data.items():
        p.drawString(120, y, f"{key}: {value}")
        y -= 20

    p.showPage()
    p.save()

    return response
