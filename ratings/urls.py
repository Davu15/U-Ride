from django.urls import path
from . import views

app_name = 'ratings'

urlpatterns = [
    path('trip/<int:trip_id>/rate/', views.rate_users, name='rate_users'),
]
