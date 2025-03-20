from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FinancialGoal
from .forms import FinancialGoalForm

@login_required
def goals_list(request):
    goals = FinancialGoal.objects.filter(user=request.user).order_by('-target_date')  
    return render(request, 'goals/list.html', {'goals': goals})

@login_required
def add_goal(request):
    if request.method == "POST":
        form = FinancialGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user

            if goal.target_amount <= 0:
                messages.error(request, "Сума цілі повинна бути більше 0.")
            elif goal.target_amount > 10**6:  
                messages.error(request, "Сума цілі надто велика.")
            else:
                goal.save()
                messages.success(request, "Ціль успішно додана!")
                return redirect('goals:goals_list')
    else:
        form = FinancialGoalForm()

    return render(request, 'goals/add.html', {'form': form})
