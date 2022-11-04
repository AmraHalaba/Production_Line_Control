from django.urls import path

from .views import *

app_name = 'reports'

urlpatterns = [
    path('', HomeView.as_view(), name="home-view"),
    
    path('reports/', SelectView.as_view(), name="select-report"),
    path('reports/summary/', main_report_summary, name="summary-view"),
    
    path('<str:production_line>/', report_view, name="report-view"),
    path('reports/delete_view/<str:pk>/', delete_view, name="delete-view"),
    path('<str:production_line>/<str:pk>/update/', ReportUpdateView.as_view(), name="update-view"),
    
    
]

