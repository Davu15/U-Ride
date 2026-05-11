from django.contrib import admin
from .models import Reporte, HistorialEventos, ConfiguracionSistema


class ReporteAdmin(admin.ModelAdmin):
    list_display = ('reportador', 'reportado', 'motivo', 'estado', 'fecha_reporte')
    list_filter = ('estado', 'motivo', 'fecha_reporte')
    search_fields = ('reportador__correo_institucional', 'reportado__correo_institucional')
    readonly_fields = ('fecha_reporte',)
    actions = ['marcar_revisado', 'marcar_resuelto']
    
    def marcar_revisado(self, request, queryset):
        """Acción para marcar reportes como en revisión."""
        updated = queryset.update(estado='En revisión', revisado_por=request.user)
        self.message_user(request, f'{updated} reportes marcados como en revisión')
    
    def marcar_resuelto(self, request, queryset):
        """Acción para marcar reportes como resueltos."""
        updated = queryset.update(estado='Resuelto', revisado_por=request.user)
        self.message_user(request, f'{updated} reportes marcados como resueltos')
    
    marcar_revisado.short_description = "Marcar como en revisión"
    marcar_resuelto.short_description = "Marcar como resuelto"


class HistorialEventosAdmin(admin.ModelAdmin):
    list_display = ('tipo_evento', 'usuario', 'fecha_evento')
    list_filter = ('tipo_evento', 'fecha_evento')
    search_fields = ('usuario__correo_institucional', 'descripcion')
    readonly_fields = ('fecha_evento',)


class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Control de Comportamiento', {
            'fields': ('limite_advertencias', 'dias_suspension')
        }),
        ('Seguridad', {
            'fields': ('edad_minima', 'reglas_seguridad')
        }),
    )


admin.site.register(Reporte, ReporteAdmin)
admin.site.register(HistorialEventos, HistorialEventosAdmin)
admin.site.register(ConfiguracionSistema, ConfiguracionSistemaAdmin)
