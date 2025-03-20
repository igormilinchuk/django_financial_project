from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from income.models import Income
from .forms import IncomeForm

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            
            # Валідація даних
            if income.amount <= 0:
                messages.error(request, "Сума повинна бути більшою за нуль.")
            elif income.date_received > now().date():
                messages.error(request, "Дата не може бути в майбутньому.")
            else:
                income.save()
                messages.success(request, "Дохід успішно додано!")
                return redirect('income:income_history')
    else:
        form = IncomeForm()

    return render(request, 'income/add_income.html', {'form': form})

@login_required
def income_history(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date_received')
    total_income = sum(income.amount for income in incomes)  # Підрахунок загальної суми
    return render(request, 'income/income_history.html', {'incomes': incomes, 'total_income': total_income})
