from django.db import models
from django.utils import timezone
from users.models import Usuario
from trips.models import Viaje


class Reporte(models.Model):
    """Modelo para reportes de conducta indebida."""
    
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En revisión', 'En revisión'),
        ('Resuelto', 'Resuelto'),
    ]
    
    MOTIVO_CHOICES = [
        ('Conducta agresiva', 'Conducta agresiva'),
        ('Incumplimiento de reglas', 'Incumplimiento de reglas'),
        ('Mala condición del vehículo', 'Mala condición del vehículo'),
        ('Abuso o acoso', 'Abuso o acoso'),
        ('Daños a vehículo', 'Daños a vehículo'),
        ('Llegada tardía', 'Llegada tardía'),
        ('No presentarse', 'No presentarse'),
        ('Otro', 'Otro'),
    ]
    
    reportador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='reportes_realizados',
        help_text="Usuario que realiza el reporte"
    )
    
    reportado = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='reportes_recibidos',
        help_text="Usuario siendo reportado"
    )
    
    viaje = models.ForeignKey(
        Viaje,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reportes',
        help_text="Viaje asociado al reporte"
    )
    
    motivo = models.CharField(
        max_length=50,
        choices=MOTIVO_CHOICES,
        help_text="Motivo del reporte"
    )
    
    descripcion = models.TextField(
        help_text="Descripción detallada del incidente"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Pendiente',
        help_text="Estado del reporte"
    )
    
    # Administración del reporte
    revisado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reportes_revisados',
        help_text="Administrador que revisó el reporte"
    )
    
    accion_tomada = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Acción tomada (advertencia, suspensión, etc.)"
    )
    
    # Metadatos
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Fecha en que se revisó el reporte"
    )
    
    class Meta:
        db_table = 'reporte'
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        ordering = ['-fecha_reporte']
    
    def __str__(self):
        return f"Reporte de {self.reportador} contra {self.reportado} ({self.motivo})"


class HistorialEventos(models.Model):
    """Modelo para trazabilidad de eventos del sistema."""
    
    TIPO_EVENTO_CHOICES = [
        ('Registro', 'Registro'),
        ('Login', 'Login'),
        ('Viaje Creado', 'Viaje Creado'),
        ('Viaje Cancelado', 'Viaje Cancelado'),
        ('Solicitud Aceptada', 'Solicitud Aceptada'),
        ('Solicitud Rechazada', 'Solicitud Rechazada'),
        ('Calificación', 'Calificación'),
        ('Reporte', 'Reporte'),
        ('Advertencia', 'Advertencia'),
        ('Suspensión', 'Suspensión'),
        ('Otro', 'Otro'),
    ]
    
    tipo_evento = models.CharField(
        max_length=50,
        choices=TIPO_EVENTO_CHOICES,
        help_text="Tipo de evento"
    )
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='historial_eventos',
        help_text="Usuario involucrado en el evento"
    )
    
    descripcion = models.TextField(
        help_text="Descripción del evento"
    )
    
    detalles = models.JSONField(
        blank=True,
        null=True,
        help_text="Detalles adicionales en formato JSON"
    )
    
    # Metadatos
    fecha_evento = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'historial_eventos'
        verbose_name = 'Historial de Evento'
        verbose_name_plural = 'Historial de Eventos'
        ordering = ['-fecha_evento']
    
    def __str__(self):
        return f"{self.tipo_evento} - {self.usuario} ({self.fecha_evento.strftime('%d/%m/%Y %H:%M')})"


class ConfiguracionSistema(models.Model):
    """Modelo singleton para configuración global del sistema."""
    
    # Límites de advertencias
    limite_advertencias = models.IntegerField(
        default=3,
        help_text="Número de advertencias antes de suspender"
    )
    
    # Duración de suspensión (en días)
    dias_suspension = models.IntegerField(
        default=7,
        help_text="Días de suspensión por cada advertencia"
    )
    
    # Reglas de seguridad
    reglas_seguridad = models.TextField(
        default="1. Respetar horarios acordados.\n2. Comportamiento cordial.\n3. Cuidado del vehículo.",
        help_text="Reglas de seguridad del sistema"
    )
    
    # Restricciones
    edad_minima = models.IntegerField(
        default=18,
        help_text="Edad mínima permitida"
    )
    
    class Meta:
        db_table = 'configuracion_sistema'
        verbose_name = 'Configuración del Sistema'
        
        def __str__(self):
            return "Configuración del Sistema"
    
    @classmethod
    def get_configuracion(cls):
        """Obtiene la configuración global (singleton)."""
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
