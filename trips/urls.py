from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    # Conducción
    path('publish/', views.publish_trip, name='publish_trip'),
    path('my-trips/', views.my_trips, name='my_trips'),
    path('trip/<int:trip_id>/requests/', views.trip_requests, name='trip_requests'),
    path('request/<int:request_id>/accept/', views.accept_request, name='accept_request'),
    path('request/<int:request_id>/reject/', views.reject_request, name='reject_request'),
    
    # Búsqueda de viajes
    path('search/', views.search_trips, name='search_trips'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:trip_id>/request/', views.request_trip, name='request_trip'),
]
