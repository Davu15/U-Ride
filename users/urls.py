from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Autenticación
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('verify-email/reenviar/', views.reenviar_codigo, name='reenviar_codigo'),
    
    # Recuperación de Contraseña
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-code/', views.verify_reset_code, name='verify_reset_code'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
    # Perfil
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/vehicle/', views.register_vehicle, name='register_vehicle'),
]
