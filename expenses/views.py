from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import Expense
from .forms import ExpenseForm

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            
            # Валідація введених даних
            if expense.amount <= 0:
                messages.error(request, "Сума витрати повинна бути більше 0.")
            elif expense.date > now().date():
                messages.error(request, "Дата витрати не може бути у майбутньому.")
            else:
                expense.save()
                messages.success(request, "Витрату успішно додано!")
                return redirect('expenses:expenses_list')
    else:
        form = ExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def expenses_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total_expense = sum(exp.amount for exp in expenses)  

    return render(request, 'expenses/expenses_list.html', {
        'expenses': expenses,
        'total_expense': total_expense
    })
