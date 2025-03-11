from django.urls import path
from . import views

app_name = 'income'

urlpatterns = [
    path('add/', views.add_income, name='add_income'),
    path('history/', views.income_history, name='income_history'),
]
