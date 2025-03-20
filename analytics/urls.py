from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path("generate/<str:report_type>/", views.generate_report, name="generate_report"),
]
