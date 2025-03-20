from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.report_dashboard, name='report_dashboard'),
    path('generate/', views.generate_report, name='generate_report'),

    path('generate/<int:report_id>/pdf/', views.export_report_pdf, name='export_report_pdf'),
]
