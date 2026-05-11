from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import Usuario
from trips.models import Viaje


class Calificacion(models.Model):
    """Modelo para calificaciones entre usuarios."""
    
    TIPO_CHOICES = [
        ('Conductor a Pasajero', 'Conductor a Pasajero'),
        ('Pasajero a Conductor', 'Pasajero a Conductor'),
    ]
    
    viaje = models.ForeignKey(
        Viaje,
        on_delete=models.CASCADE,
        related_name='calificaciones',
        help_text="Viaje en el que se produce la calificación"
    )
    
    evaluador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='calificaciones_realizadas',
        help_text="Usuario que realiza la calificación"
    )
    
    evaluado = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='calificaciones_recibidas',
        help_text="Usuario que recibe la calificación"
    )
    
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Puntuación de 1 a 5 estrellas"
    )
    
    resena = models.TextField(
        blank=True,
        null=True,
        help_text="Reseña opcional sobre la experiencia"
    )
    
    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES,
        help_text="Tipo de calificación"
    )
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'calificacion'
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        ordering = ['-fecha_creacion']
        unique_together = ('viaje', 'evaluador', 'evaluado')
    
    def __str__(self):
        return f"{self.evaluador} → {self.evaluado}: {self.puntuacion} ⭐"
    
    def save(self, *args, **kwargs):
        """Actualizar la reputación del usuario evaluado."""
        super().save(*args, **kwargs)
        
        # Recalcular promedio de reputación
        calificaciones = Calificacion.objects.filter(evaluado=self.evaluado)
        if calificaciones.exists():
            promedio = sum(cal.puntuacion for cal in calificaciones) / calificaciones.count()
            self.evaluado.reputacion = round(promedio, 2)
            self.evaluado.save()
