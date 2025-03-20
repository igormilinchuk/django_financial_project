from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FinancialGoal, GoalContribution
from .forms import FinancialGoalForm, GoalContributionForm



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

@login_required
def update_goal_progress(request, goal_id):
    goal = get_object_or_404(FinancialGoal, id=goal_id, user=request.user)

    if request.method == "POST":
        form = GoalContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.goal = goal

            if goal.current_amount + contribution.amount > goal.target_amount:
                messages.error(request, "Не можна внести більше, ніж потрібно для досягнення цілі!")
            else:
                contribution.save()  
                messages.success(request, "Внесок додано успішно! Витрати оновлено.")
            
            return redirect("goals:goals_list")

    else:
        form = GoalContributionForm()

    return render(request, "goals/update_goal.html", {"form": form, "goal": goal})

