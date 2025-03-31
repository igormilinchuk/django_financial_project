"""
URL configuration for financial_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('user/', include(('users.urls', 'users'), namespace='user')),
    path('income/', include(('income.urls', 'income'), namespace='income')),
    path('goals/', include(('goals.urls', 'goals'), namespace='goals')),
    path('expenses/', include(('expenses.urls', 'expenses'), namespace='expenses')),
    path('analytics/', include(('analytics.urls', 'analytics'), namespace='analytics')),
]
