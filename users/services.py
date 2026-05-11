"""
Servicio de verificación de correo institucional.
Gestiona la generación, envío y validación de códigos de verificación.
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Usuario
import logging

logger = logging.getLogger(__name__)


def generar_y_enviar_codigo(usuario):
    """
    Genera un código de verificación y lo envía al correo del usuario.
    
    Args:
        usuario (Usuario): Instancia del usuario a verificar
    
    Returns:
        tuple: (success: bool, mensaje: str)
    """
    try:
        # Generar código
        codigo = usuario.generar_codigo_verificacion()
        
        # Construir mensaje
        asunto = f"Código de Verificación U-Ride - {codigo}"
        mensaje_texto = f"""
Bienvenido a U-Ride!

Tu código de verificación es: {codigo}

Este código es válido por 24 horas. No compartas este código con nadie.

Si no solicitaste este código, ignora este mensaje.

---
U-Ride - Sistema de Transporte Colaborativo
"""
        
        mensaje_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="background-color: #f4f4f4; padding: 20px; border-radius: 5px;">
                    <h2 style="color: #2c3e50;">¡Bienvenido a U-Ride!</h2>
                    
                    <p>Tu código de verificación es:</p>
                    
                    <div style="background-color: #27ae60; color: white; padding: 20px; border-radius: 5px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 2px; margin: 20px 0;">
                        {codigo}
                    </div>
                    
                    <p><strong>Instrucciones:</strong></p>
                    <ol>
                        <li>Copia el código anterior</li>
                        <li>Ingresa a la página de verificación</li>
                        <li>Pega el código en el campo correspondiente</li>
                    </ol>
                    
                    <p style="color: #e74c3c;"><strong>⏱️ Nota:</strong> Este código es válido por 24 horas.</p>
                    <p style="color: #e74c3c;"><strong>🔒 Seguridad:</strong> No compartas este código con nadie.</p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    <p style="color: #7f8c8d; font-size: 12px;">
                        Si no solicitaste este código, puedes ignorar este mensaje.
                    </p>
                </div>
            </body>
        </html>
        """
        
        # Enviar email
        send_mail(
            subject=asunto,
            message=mensaje_texto,
            from_email=settings.EMAIL_FROM,
            recipient_list=[usuario.correo_institucional],
            html_message=mensaje_html,
            fail_silently=False,
        )
        
        # Log en consola (visible incluso con console backend)
        print("\n" + "="*80)
        print("📧 EMAIL DE VERIFICACIÓN ENVIADO")
        print("="*80)
        print(f"Para: {usuario.correo_institucional}")
        print(f"Usuario: {usuario.get_full_name()}")
        print(f"Código: {codigo}")
        print("="*80 + "\n")
        
        logger.info(f"Código de verificación enviado a {usuario.correo_institucional}")
        
        return True, f"Código enviado a {usuario.correo_institucional}"
    
    except Exception as e:
        logger.error(f"Error al enviar código de verificación: {str(e)}")
        return False, f"Error al enviar el código: {str(e)}"


def verificar_usuario(correo, codigo):
    """
    Verifica el código ingresado por el usuario.
    
    Args:
        correo (str): Correo institucional del usuario
        codigo (str): Código ingresado por el usuario
    
    Returns:
        tuple: (success: bool, usuario: Usuario|None, mensaje: str)
    """
    try:
        usuario = Usuario.objects.get(correo_institucional=correo.lower())
        
        if usuario.verificado:
            return False, None, "Este usuario ya está verificado"
        
        if usuario.verificar_codigo(codigo):
            logger.info(f"Usuario verificado: {correo}")
            print("\n" + "="*80)
            print("✅ USUARIO VERIFICADO EXITOSAMENTE")
            print("="*80)
            print(f"Correo: {correo}")
            print(f"Usuario: {usuario.get_full_name()}")
            print("El usuario puede iniciar sesión ahora")
            print("="*80 + "\n")
            
            return True, usuario, "Correo verificado exitosamente"
        else:
            return False, None, "Código incorrecto"
    
    except Usuario.DoesNotExist:
        return False, None, "Usuario no encontrado"
    
    except Exception as e:
        logger.error(f"Error al verificar usuario: {str(e)}")
        return False, None, f"Error al verificar: {str(e)}"


def enviar_codigo_reintento(correo):
    """
    Envía un nuevo código si el usuario no ha recibido el anterior.
    
    Args:
        correo (str): Correo institucional del usuario
    
    Returns:
        tuple: (success: bool, mensaje: str)
    """
    try:
        usuario = Usuario.objects.get(correo_institucional=correo.lower())
        
        if usuario.verificado:
            return False, "Este usuario ya está verificado"
        
        return generar_y_enviar_codigo(usuario)
    
    except Usuario.DoesNotExist:
        return False, "Usuario no encontrado"
    
    except Exception as e:
        logger.error(f"Error al reenviar código: {str(e)}")
        return False, f"Error al reenviar: {str(e)}"


# ============================================================================
# SERVICIOS DE RECUPERACIÓN DE CONTRASEÑA
# ============================================================================

def generar_y_enviar_codigo_recuperacion(correo):
    """
    Genera y envía un código de recuperación de contraseña.
    
    Args:
        correo (str): Correo institucional del usuario
    
    Returns:
        tuple: (success: bool, mensaje: str)
    """
    try:
        usuario = Usuario.objects.get(correo_institucional=correo.lower())
        
        # Generar código de recuperación
        codigo = usuario.generar_codigo_recuperacion()
        
        # Construir mensaje
        asunto = f"Código de Recuperación de Contraseña U-Ride - {codigo}"
        mensaje_texto = f"""
Solicitud de Recuperación de Contraseña - U-Ride

Tu código de recuperación es: {codigo}

Este código es válido por 24 horas. No compartas este código con nadie.

Pasos para recuperar tu contraseña:
1. Ingresa el código que recibiste
2. Crea una nueva contraseña segura
3. Confirma tu nueva contraseña

Si no solicitaste recuperar tu contraseña, ignora este mensaje.

---
U-Ride - Sistema de Transporte Colaborativo
"""
        
        mensaje_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="background-color: #f4f4f4; padding: 20px; border-radius: 5px;">
                    <h2 style="color: #2c3e50;">Recuperación de Contraseña</h2>
                    
                    <p>Has solicitado recuperar tu contraseña en U-Ride.</p>
                    
                    <p>Tu código de recuperación es:</p>
                    
                    <div style="background-color: #e74c3c; color: white; padding: 20px; border-radius: 5px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 2px; margin: 20px 0;">
                        {codigo}
                    </div>
                    
                    <p><strong>Instrucciones:</strong></p>
                    <ol>
                        <li>Copia el código anterior</li>
                        <li>Ingresa a la página de recuperación de contraseña</li>
                        <li>Pega el código en el campo correspondiente</li>
                        <li>Crea una nueva contraseña segura</li>
                    </ol>
                    
                    <p style="color: #e74c3c;"><strong>⏱️ Nota:</strong> Este código es válido por 24 horas.</p>
                    <p style="color: #e74c3c;"><strong>🔒 Seguridad:</strong> No compartas este código con nadie.</p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    <p style="color: #7f8c8d; font-size: 12px;">
                        Si no solicitaste recuperar tu contraseña, puedes ignorar este mensaje.
                    </p>
                </div>
            </body>
        </html>
        """
        
        # Enviar email
        send_mail(
            subject=asunto,
            message=mensaje_texto,
            from_email=settings.EMAIL_FROM,
            recipient_list=[usuario.correo_institucional],
            html_message=mensaje_html,
            fail_silently=False,
        )
        
        # Log en consola
        print("\n" + "="*80)
        print("🔐 CÓDIGO DE RECUPERACIÓN DE CONTRASEÑA")
        print("="*80)
        print(f"Para: {usuario.correo_institucional}")
        print(f"Usuario: {usuario.get_full_name()}")
        print(f"Código: {codigo}")
        print("Válido por: 24 horas")
        print("="*80 + "\n")
        
        logger.info(f"Código de recuperación enviado a {usuario.correo_institucional}")
        
        return True, f"Código de recuperación enviado a {usuario.correo_institucional}"
    
    except Usuario.DoesNotExist:
        return False, "Usuario no encontrado"
    
    except Exception as e:
        logger.error(f"Error al generar código de recuperación: {str(e)}")
        return False, f"Error al enviar el código: {str(e)}"


def verificar_codigo_recuperacion(correo, codigo):
    """
    Verifica el código de recuperación ingresado.
    
    Args:
        correo (str): Correo institucional del usuario
        codigo (str): Código ingresado por el usuario
    
    Returns:
        tuple: (success: bool, mensaje: str)
    """
    try:
        usuario = Usuario.objects.get(correo_institucional=correo.lower())
        es_valido, mensaje = usuario.verificar_codigo_recuperacion(codigo)
        
        if es_valido:
            logger.info(f"Código de recuperación verificado: {correo}")
            print("\n" + "="*80)
            print("✅ CÓDIGO DE RECUPERACIÓN VERIFICADO")
            print("="*80)
            print(f"Correo: {correo}")
            print("El usuario puede proceder a cambiar su contraseña")
            print("="*80 + "\n")
        
        return es_valido, mensaje
    
    except Usuario.DoesNotExist:
        return False, "Usuario no encontrado"
    
    except Exception as e:
        logger.error(f"Error al verificar código de recuperación: {str(e)}")
        return False, f"Error al verificar: {str(e)}"


def cambiar_contrasena_recuperacion(correo, nueva_contrasena):
    """
    Cambia la contraseña del usuario después de verificar el código.
    
    Args:
        correo (str): Correo institucional del usuario
        nueva_contrasena (str): Nueva contraseña
    
    Returns:
        tuple: (success: bool, mensaje: str)
    """
    try:
        usuario = Usuario.objects.get(correo_institucional=correo.lower())
        
        # Verificar que el código sea válido
        if not usuario.codigo_recuperacion_valido():
            return False, "No hay una solicitud de recuperación activa"
        
        # Cambiar contraseña
        usuario.set_password(nueva_contrasena)
        usuario.limpiar_codigo_recuperacion()
        usuario.save()
        
        logger.info(f"Contraseña cambiada: {correo}")
        print("\n" + "="*80)
        print("✅ CONTRASEÑA CAMBIADA EXITOSAMENTE")
        print("="*80)
        print(f"Correo: {correo}")
        print("Ahora puedes iniciar sesión con tu nueva contraseña")
        print("="*80 + "\n")
        
        return True, "Contraseña cambiada exitosamente"
    
    except Usuario.DoesNotExist:
        return False, "Usuario no encontrado"
    
    except Exception as e:
        logger.error(f"Error al cambiar contraseña: {str(e)}")
        return False, f"Error al cambiar la contraseña: {str(e)}"
