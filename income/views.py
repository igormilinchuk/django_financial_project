from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import Income
from .forms import IncomeForm

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.date = now().date()
            
            print(f"Amount: {income.amount}, Date: {income.date}")  # Додайте для перевірки значення

            if income.amount <= 0:
                messages.error(request, "Сума повинна бути більшою за нуль.")
                print("Error: Amount is less than or equal to zero.")  # Додайте для перевірки
            elif income.date and income.date > now().date():
                messages.error(request, "Дата не може бути в майбутньому.")
                print("Error: Date is in the future.")  # Додайте для перевірки
            else:
                income.save()
                messages.success(request, "Дохід успішно додано!")
                print("Income saved successfully!")  # Додайте для перевірки
                return redirect('income:income_history')
        else:
            print(f"Form is not valid: {form.errors}")  # Вивести помилки форми, якщо є
    else:
        form = IncomeForm()

    return render(request, 'income/add_income.html', {'form': form})

@login_required
def income_history(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    total_income = sum(income.amount for income in incomes)  
    return render(request, 'income/income_history.html', {'incomes': incomes, 'total_income': total_income})
