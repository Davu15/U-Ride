from django.contrib import admin
from .models import Calificacion


class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('evaluador', 'evaluado', 'puntuacion', 'tipo', 'fecha_creacion')
    list_filter = ('puntuacion', 'tipo', 'fecha_creacion')
    search_fields = ('evaluador__correo_institucional', 'evaluado__correo_institucional')
    readonly_fields = ('fecha_creacion',)


admin.site.register(Calificacion, CalificacionAdmin)
