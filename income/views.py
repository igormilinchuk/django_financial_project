from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from income.models import Income
from .forms import IncomeForm

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  
            income.save()
            return redirect('income:income_history')
    else:
        form = IncomeForm()

    return render(request, 'income/add_income.html', {'form': form})

@login_required
def income_history(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date_received')
    return render(request, 'income/income_history.html', {'incomes': incomes})
