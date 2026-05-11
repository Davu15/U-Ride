from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Vehiculo


class UsuarioAdmin(UserAdmin):
    """Personalización del admin para el modelo Usuario."""
    
    model = Usuario
    
    list_display = (
        'correo_institucional',
        'get_full_name',
        'verificado',
        'reputacion',
        'cantidad_viajes',
        'advertencias',
        'esta_suspendido'
    )
    
    list_filter = ('verificado', 'fecha_creacion', 'advertencias')
    
    search_fields = ('correo_institucional', 'first_name', 'last_name')
    
    fieldsets = (
        ('Información de Autenticación', {
            'fields': ('correo_institucional', 'username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'carrera', 'numero_contacto', 'zona_referencia', 'foto_perfil')
        }),
        ('Verificación y Seguridad', {
            'fields': ('verificado', 'codigo_verificacion')
        }),
        ('Reputación y Viajes', {
            'fields': ('reputacion', 'cantidad_viajes')
        }),
        ('Control de Comportamiento', {
            'fields': ('advertencias', 'suspendido_hasta')
        }),
        ('Permisos', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'ultima_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('fecha_creacion', 'ultima_actualizacion', 'username')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo_institucional', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


class VehiculoAdmin(admin.ModelAdmin):
    """Personalización del admin para el modelo Vehiculo."""
    
    list_display = ('placa', 'marca', 'modelo', 'usuario', 'capacidad_asientos', 'activo')
    list_filter = ('activo', 'ano', 'fecha_registro')
    search_fields = ('placa', 'marca', 'modelo', 'usuario__correo_institucional')
    readonly_fields = ('fecha_registro',)


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Vehiculo, VehiculoAdmin)
