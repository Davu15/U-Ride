from django.contrib import admin
from .models import Viaje, SolicitudViaje


class SolicitudViajeInline(admin.TabularInline):
    model = SolicitudViaje
    extra = 0
    readonly_fields = ('fecha_solicitud', 'fecha_respuesta')


class ViajeAdmin(admin.ModelAdmin):
    list_display = ('zona_origen', 'zona_destino', 'conductor', 'fecha_hora_salida', 'cupos_disponibles', 'estado')
    list_filter = ('estado', 'fecha_hora_salida', 'fecha_creacion')
    search_fields = ('zona_origen', 'zona_destino', 'conductor__correo_institucional')
    readonly_fields = ('fecha_creacion', 'ultima_actualizacion')
    inlines = [SolicitudViajeInline]


class SolicitudViajeAdmin(admin.ModelAdmin):
    list_display = ('pasajero', 'viaje', 'estado', 'fecha_solicitud')
    list_filter = ('estado', 'fecha_solicitud')
    search_fields = ('pasajero__correo_institucional', 'viaje__zona_origen', 'viaje__zona_destino')
    readonly_fields = ('fecha_solicitud',)


admin.site.register(Viaje, ViajeAdmin)
admin.site.register(SolicitudViaje, SolicitudViajeAdmin)
