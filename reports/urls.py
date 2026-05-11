from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('trip/<int:trip_id>/report/', views.report_user, name='report_user'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('report/<int:report_id>/review/', views.review_report, name='review_report'),
    path('users/', views.manage_users, name='manage_users'),
]
