from django.db import models
from django.utils import timezone
from users.models import Usuario, Vehiculo


class Viaje(models.Model):
    """Modelo para los viajes compartidos."""
    
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('En Curso', 'En Curso'),
        ('Finalizado', 'Finalizado'),
        ('Cancelado', 'Cancelado'),
    ]
    
    conductor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='viajes_como_conductor',
        help_text="Conductor del viaje"
    )
    
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Vehículo usado en el viaje"
    )
    
    zona_origen = models.CharField(
        max_length=100,
        help_text="Zona o barrio de origen"
    )
    
    zona_destino = models.CharField(
        max_length=100,
        help_text="Zona o barrio de destino"
    )
    
    fecha_hora_salida = models.DateTimeField(
        help_text="Fecha y hora de salida"
    )
    
    cupos_totales = models.IntegerField(
        help_text="Cantidad total de cupos (sin incluir conductor)"
    )
    
    cupos_disponibles = models.IntegerField(
        help_text="Cupos disponibles en el momento"
    )
    
    notas_reglas = models.TextField(
        blank=True,
        null=True,
        help_text="Notas o reglas especiales del viaje"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Activo',
        help_text="Estado actual del viaje"
    )
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'viaje'
        verbose_name = 'Viaje'
        verbose_name_plural = 'Viajes'
        ordering = ['-fecha_hora_salida']
    
    def __str__(self):
        return f"{self.zona_origen} → {self.zona_destino} ({self.fecha_hora_salida.strftime('%d/%m/%Y %H:%M')})"


class SolicitudViaje(models.Model):
    """Modelo para solicitudes de pasajeros a viajes."""
    
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Rechazada', 'Rechazada'),
        ('Cancelada', 'Cancelada'),
    ]
    
    viaje = models.ForeignKey(
        Viaje,
        on_delete=models.CASCADE,
        related_name='solicitudes_pasajeros',
        help_text="Viaje solicitado"
    )
    
    pasajero = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='solicitudes_viajes',
        help_text="Pasajero que solicita"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Pendiente',
        help_text="Estado de la solicitud"
    )
    
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Fecha en que el conductor respondió"
    )
    
    class Meta:
        db_table = 'solicitud_viaje'
        verbose_name = 'Solicitud de Viaje'
        verbose_name_plural = 'Solicitudes de Viaje'
        unique_together = ('viaje', 'pasajero')  # Un pasajero no puede solicitar dos veces el mismo viaje
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"{self.pasajero.correo_institucional} → {self.viaje} ({self.estado})"
