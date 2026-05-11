# Contexto del Proyecto: U-Ride
Actúa como un desarrollador experto en Python, Django y diseño frontend. Necesito que me ayudes a desarrollar un sistema web llamado "U-Ride", el cual es una plataforma de transporte seguro compartido (carpooling) exclusivo para estudiantes de una misma institución. 

El objetivo es permitir a los estudiantes publicar y unirse a viajes compartidos de manera segura, controlada y organizada, priorizando la verificación institucional y el comportamiento responsable.

## Stack Tecnológico
* **Backend:** Python con Django.
* **Frontend:** HTML, CSS, JavaScript básico.
* **Framework de Diseño:** Bootstrap (importado vía CDN para mayor facilidad).
* **Base de Datos:** MySQL.

## Roles del Sistema
El sistema cuenta con tres roles principales:
1. **Estudiante (Pasajero):** Busca viajes, solicita unirse y califica conductores.
2. **Estudiante (Conductor/a):** Registra su vehículo, publica viajes, acepta/rechaza solicitudes de pasajeros y califica. *Nota: Un estudiante puede actuar como pasajero y conductor.*
3. **Administrador/a:** Gestiona reportes, revisa usuarios infractores (advertencias/suspensiones) y configura parámetros generales.

## Modelos de Base de Datos (Estructura Sugerida para Django)
Necesito que generes los siguientes modelos en `models.py`:

* **Usuario (Custom User):** Hereda de `AbstractUser`. Campos: correo institucional (único y obligatorio para login), contraseña, nombre completo, carrera, número de contacto (opcional), zona/barrio de referencia, foto de perfil (opcional), estado de verificación (booleano), reputación (promedio), cantidad_viajes, advertencias, suspendido_hasta (fecha).
* **Vehículo:** Usuario (ForeignKey), marca, modelo, año, color, placa (única), capacidad_asientos.
* **Viaje:** Conductor (ForeignKey a Usuario), vehículo (ForeignKey), zona_origen, zona_destino, fecha_hora_salida, cupos_totales, cupos_disponibles, notas_reglas, estado (Activo, En Curso, Finalizado, Cancelado).
* **SolicitudViaje:** Viaje (ForeignKey), pasajero (ForeignKey a Usuario), estado (Pendiente, Confirmada, Rechazada, Cancelada), fecha_solicitud.
* **Calificacion:** Viaje (ForeignKey), evaluador (ForeignKey a Usuario), evaluado (ForeignKey a Usuario), puntuacion (1 a 5 estrellas), resena (texto opcional), tipo (Conductor a Pasajero, o Pasajero a Conductor).
* **Reporte:** Reportador (ForeignKey), reportado (ForeignKey), viaje (ForeignKey), motivo, descripcion, estado (Pendiente, En revisión, Resuelto).
* **HistorialEventos (Trazabilidad):** Acción, usuario, fecha, detalles.
* **ConfiguracionSistema:** Singleton para parámetros como límite de advertencias, reglas de seguridad de texto, etc.

## Requerimientos Funcionales Básicos (Views & Templates)
Necesito que me ayudes a implementar las siguientes vistas y flujos utilizando `views.py` y plantillas de Django renderizadas con Bootstrap:

1.  **Autenticación (RF1):** Registro y Login usando *únicamente* correo institucional. La cuenta debe verificarse mediante un código de 6 dígitos enviado por correo electrónico.
2.  **Gestión de Perfil (RF2):** Vista para ver y editar el perfil (CRUD de datos personales) y para registrar un vehículo si desea ser conductor.
3.  **Módulo de Conductores (RF3 & RF6):**
    * Formulario para publicar un viaje (origen, destino por zonas, fecha/hora, cupos).
    * Panel de "Mis Viajes" para ver viajes creados y listar las solicitudes de pasajeros pendientes.
    * Botones para "Aceptar" (resta un cupo) o "Rechazar" solicitudes.
4.  **Módulo de Pasajeros (RF4 & RF5):**
    * Buscador de viajes con filtros por zona, fecha, hora y disponibilidad de cupos.
    * Detalle del viaje con botón para "Solicitar Unirse".
5.  **Post-Viaje y Calificación (RF8 & RF10):**
    * Pantalla para que, tras finalizar el viaje, se puedan dejar estrellas y reseñas.
    * Opción para "Reportar" conducta indebida adjuntando un motivo.
6.  **Panel de Administrador (RF11):**
    * Dashboard con estadísticas.
    * Gestión de reportes (Advertir usuario o Suspender temporalmente).
    * Visualizar historial de eventos (trazabilidad).

## Reglas de Negocio y Seguridad (Importante)
* **Privacidad (RNF2):** Las ubicaciones se manejan por zonas o barrios, **no** por coordenadas exactas obligatorias o direcciones de domicilio precisas.
* **Restricción de Acceso:** El sistema restringe el acceso a quienes no tengan el dominio de correo de la institución o estén suspendidos.
* **Contraseñas (RNF1):** Deben estar encriptadas (Django lo hace por defecto, pero asegúrate de validarlo).

## Instrucciones para empezar
Por favor, actúa como mi compañero de programación. Para empezar:
1. Genera la configuración inicial del modelo `Usuario` personalizado en `models.py`.
2. Dame la estructura base del `settings.py` para soportar la base de datos MySQL y las plantillas estáticas con Bootstrap CDN.
3. Espera mis instrucciones para ir creando aplicación por aplicación (ej. primero 'users', luego 'trips', luego 'admin_panel').