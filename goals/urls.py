from django.urls import path
from .views import goals_list, add_goal

urlpatterns = [
    path('list/', goals_list, name='goals_list'),
    path('add/', add_goal, name='add_goal'),
]
