from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('add/', views.add_expense, name='add_expense'),
    path('history/', views.expenses_list, name='expenses_list'),
]
