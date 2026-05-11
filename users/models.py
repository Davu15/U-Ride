from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import random
import string


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que hereda de AbstractUser.
    Incluye campos adicionales para el sistema U-Ride.
    """
    
    # Campo de email institucional (login)
    correo_institucional = models.EmailField(
        unique=True,
        help_text="Correo institucional para login (ej: usuario@uta.edu.ec)"
    )
    
    # Información personal
    carrera = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Carrera o programa académico"
    )
    
    numero_contacto = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Número de teléfono o celular"
    )
    
    zona_referencia = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Zona o barrio de referencia"
    )
    
    foto_perfil = models.ImageField(
        upload_to='perfil_photos/',
        blank=True,
        null=True,
        help_text="Foto de perfil del usuario"
    )
    
    # Seguridad y verificación
    verificado = models.BooleanField(
        default=False,
        help_text="¿El usuario ha verificado su correo institucional?"
    )
    
    codigo_verificacion = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        help_text="Código de 6 dígitos para verificar correo"
    )
    
    # Recuperación de contraseña
    codigo_recuperacion = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        help_text="Código de 6 dígitos para recuperar contraseña"
    )
    
    fecha_expiracion_recuperacion = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Fecha y hora de expiración del código de recuperación"
    )
    
    # Reputación
    reputacion = models.FloatField(
        default=5.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Puntuación promedio de reputación (0-5 estrellas)"
    )
    
    cantidad_viajes = models.IntegerField(
        default=0,
        help_text="Cantidad total de viajes completados"
    )
    
    # Control de comportamiento
    advertencias = models.IntegerField(
        default=0,
        help_text="Cantidad de advertencias acumuladas"
    )
    
    suspendido_hasta = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Fecha hasta la cual el usuario está suspendido (None si no está suspendido)"
    )
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    # Campo de username heredado de AbstractUser se usa internamente
    # Pero el login principal será por correo_institucional
    
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.correo_institucional})"
    
    def esta_suspendido(self):
        """Verifica si el usuario está actualmente suspendido."""
        from django.utils import timezone
        if self.suspendido_hasta:
            return timezone.now() < self.suspendido_hasta
        return False
    
    def puede_usar_plataforma(self):
        """Verifica si el usuario puede usar la plataforma (verificado y no suspendido)."""
        return self.verificado and not self.esta_suspendido()
    
    def generar_codigo_verificacion(self):
        """
        Genera un código de verificación de 6 dígitos.
        Retorna el código generado.
        """
        codigo = ''.join(random.choices(string.digits, k=6))
        self.codigo_verificacion = codigo
        self.save(update_fields=['codigo_verificacion'])
        return codigo
    
    def verificar_codigo(self, codigo_ingresado):
        """
        Verifica si el código ingresado coincide con el almacenado.
        Si es correcto, marca el usuario como verificado.
        
        Retorna:
            True si el código es válido
            False si no coincide o está expirado
        """
        if not self.codigo_verificacion:
            return False
        
        if self.codigo_verificacion == str(codigo_ingresado).strip():
            self.verificado = True
            self.codigo_verificacion = None
            self.save(update_fields=['verificado', 'codigo_verificacion'])
            return True
        
        return False
    
    def generar_codigo_recuperacion(self):
        """
        Genera un código de recuperación de contraseña de 6 dígitos.
        El código expira en 24 horas.
        
        Retorna:
            str: Código de 6 dígitos generado
        """
        from django.utils import timezone
        from datetime import timedelta
        
        codigo = ''.join(random.choices(string.digits, k=6))
        self.codigo_recuperacion = codigo
        self.fecha_expiracion_recuperacion = timezone.now() + timedelta(hours=24)
        self.save(update_fields=['codigo_recuperacion', 'fecha_expiracion_recuperacion'])
        return codigo
    
    def codigo_recuperacion_valido(self):
        """
        Verifica si el código de recuperación existe y no ha expirado.
        
        Retorna:
            bool: True si el código es válido y no ha expirado
        """
        from django.utils import timezone
        
        if not self.codigo_recuperacion or not self.fecha_expiracion_recuperacion:
            return False
        
        return timezone.now() < self.fecha_expiracion_recuperacion
    
    def verificar_codigo_recuperacion(self, codigo_ingresado):
        """
        Verifica si el código de recuperación ingresado es válido y no ha expirado.
        
        Args:
            codigo_ingresado (str): Código ingresado por el usuario
        
        Retorna:
            tuple: (es_valido: bool, mensaje: str)
        """
        from django.utils import timezone
        
        if not self.codigo_recuperacion:
            return False, "No hay solicitud de recuperación activa"
        
        if not self.codigo_recuperacion_valido():
            self.codigo_recuperacion = None
            self.fecha_expiracion_recuperacion = None
            self.save(update_fields=['codigo_recuperacion', 'fecha_expiracion_recuperacion'])
            return False, "El código ha expirado. Solicita uno nuevo."
        
        if self.codigo_recuperacion == str(codigo_ingresado).strip():
            return True, "Código verificado correctamente"
        
        return False, "El código es incorrecto"
    
    def limpiar_codigo_recuperacion(self):
        """
        Limpia los datos de recuperación de contraseña después de cambiarla.
        """
        self.codigo_recuperacion = None
        self.fecha_expiracion_recuperacion = None
        self.save(update_fields=['codigo_recuperacion', 'fecha_expiracion_recuperacion'])
    
    def es_dominio_institucional(email):
        """
        Valida que el correo sea del dominio institucional.
        """
        return email.lower().endswith(f"@{settings.INSTITUTIONAL_EMAIL_DOMAIN}")





class Vehiculo(models.Model):
    """
    Modelo para los vehículos registrados por conductores.
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='vehiculos',
        help_text="Conductor propietario del vehículo"
    )
    
    marca = models.CharField(max_length=50, help_text="Marca del vehículo (ej: Toyota)")
    modelo = models.CharField(max_length=50, help_text="Modelo del vehículo (ej: Corolla)")
    ano = models.IntegerField(help_text="Año del vehículo")
    color = models.CharField(max_length=30, help_text="Color del vehículo")
    placa = models.CharField(
        max_length=10,
        unique=True,
        help_text="Placa del vehículo (única)"
    )
    capacidad_asientos = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        help_text="Capacidad total de pasajeros (incluyendo conductor)"
    )
    
    # Metadatos
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'vehiculo'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
    
    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"
