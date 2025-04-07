from django.urls import path
from . import views

urlpatterns = [
    path('', views.financial_report, name='financial_report'),
    path('compare/', views.compare_report, name='compare_report'),
]
