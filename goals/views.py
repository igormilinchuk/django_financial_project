from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FinancialGoal
from .forms import FinancialGoalForm, GoalContributionForm
from datetime import timedelta
from django.utils import timezone



@login_required
def goals_history(request):
    goals = FinancialGoal.objects.filter(user=request.user).order_by('-target_date')  
    return render(request, 'goals/history.html', {'goals': goals})

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
                time_difference = goal.target_date - timezone.now().date()

                if time_difference <= timedelta(days=30):
                    goal.recurrence = 'daily'
                elif time_difference <= timedelta(days=180):
                    goal.recurrence = 'weekly'
                else:
                    goal.recurrence = 'monthly'

                goal.save()
                messages.success(request, "Ціль успішно додана!")
                return redirect('goals:history')
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
            
            return redirect("goals:history")

    else:
        form = GoalContributionForm()

    return render(request, "goals/update_goal.html", {"form": form, "goal": goal})

@login_required
def update_goal_recurrence(request, goal_id):
    goal = get_object_or_404(FinancialGoal, id=goal_id, user=request.user)

    if request.method == "POST":
        recurrence = request.POST.get('recurrence')
        
        if recurrence not in ['daily', 'weekly', 'monthly']:
            messages.error(request, "Невірний вибір періодичності.")
        else:
            goal.recurrence = recurrence
            goal.save()
            messages.success(request, "Періодичність внеску успішно оновлено!")
            return redirect('goals:history')

    return redirect('goals:history')


@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(FinancialGoal, id=goal_id, user=request.user)

    if request.method == "POST":
        goal.delete()
        messages.success(request, "Ціль успішно видалена!")
        return redirect('goals:history')

    return render(request, "goals/delete_goal.html", {"goal": goal})


