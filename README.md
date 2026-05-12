# 🚗 U-Ride - Plataforma de Carpooling Seguro para Estudiantes

<<<<<<< HEAD
##  Plataforma de Carpooling Seguro para Estudiantes
=======
U-Ride es una plataforma web diseñada para facilitar el transporte compartido seguro entre estudiantes de una misma institución, priorizando la verificación institucional y el comportamiento responsable.
>>>>>>> 5dab252 (Reorganizacion .md)

## ✨ Características Principales

<<<<<<< HEAD
##  Características Principales

✅ **Autenticación Segura:** Acceso únicamente con correo institucional verificado
✅ **Gestión de Viajes:** Publicar, buscar y solicitar viajes
✅ **Sistema de Reputación:** Calificaciones y reseñas entre usuarios
✅ **Seguridad:** Reportes y gestión administrativa de incidentes
✅ **Trazabilidad:** Historial completo de eventos del sistema
=======
- **🔐 Autenticación Segura:** Solo con correo institucional verificado por código de 6 dígitos
- **🗺️ Gestión de Viajes:** Publicar, buscar y solicitar viajes con filtros avanzados
- **⭐ Sistema de Reputación:** Calificaciones y reseñas entre usuarios
- **📋 Reportes:** Sistema de reportes y gestión administrativa de incidentes
- **📊 Trazabilidad:** Historial completo de eventos del sistema
- **🛡️ Privacidad:** Ubicaciones por zonas (no coordenadas exactas)
>>>>>>> 5dab252 (Reorganizacion .md)

##  Stack Tecnológico

- **Backend:** Django 5.0 (Python)
- **Frontend:** HTML5, CSS3, Bootstrap 5 (CDN)
- **Base de Datos:** MySQL 8.0
- **ORM:** Django ORM
- **Autenticación:** Django Auth + Custom User Model
- **Admin:** Django Admin personalizado

##  Requisitos Previos

- Python 3.8+
- MySQL 5.7+
- pip

<<<<<<< HEAD
##  Instalación y Configuración
=======
## 🚀 Instalación Rápida
>>>>>>> 5dab252 (Reorganizacion .md)

### Opción 1: Automática (Windows - RECOMENDADO)
```bash
# Solo ejecuta el script:
setup_windows.bat
```

### Opción 2: Manual (Todos los OS)

```bash
# 1. Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear base de datos MySQL
# En MySQL Workbench o console:
CREATE DATABASE u_ride_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 4. Configurar variables de entorno
# Copiar .env.example a .env y editar con tus valores:
# - DB_PASSWORD: tu contraseña de MySQL
# - SECRET_KEY: clave segura
# - EMAIL_HOST_USER y EMAIL_HOST_PASSWORD: para verificación
# - INSTITUTIONAL_EMAIL_DOMAIN: dominio de correo (ej: uta.edu.ec)

# 5. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 6. Crear superusuario (administrador)
python manage.py createsuperuser

# 7. Ejecutar servidor de desarrollo
python manage.py runserver
```

<<<<<<< HEAD
Acceder a: `http://localhost:8000`

## 📁 Estructura del Proyecto

```
U-Ride/
│
├── u_ride/                 # Configuración principal
│   ├── settings.py        # Configuraciones de Django
│   ├── urls.py            # Rutas principales
│   ├── wsgi.py            # Configuración WSGI
│   └── __init__.py
│
├── users/                 # Aplicación de usuarios
│   ├── models.py          # Usuario personalizado, Vehículo
│   ├── views.py           # Vistas de autenticación y perfil
│   ├── urls.py            # Rutas de usuarios
│   ├── admin.py           # Admin panel
│   └── templates/
│       └── users/         # Plantillas HTML
│
├── trips/                 # Aplicación de viajes
│   ├── models.py          # Viaje, SolicitudViaje
│   ├── views.py           # Vistas de búsqueda y gestión
│   ├── urls.py            # Rutas de viajes
│   ├── admin.py           # Admin panel
│   └── templates/
│       └── trips/         # Plantillas HTML
│
├── ratings/               # Aplicación de calificaciones
│   ├── models.py          # Calificación
│   ├── views.py           # Vistas de calificación
│   ├── urls.py            # Rutas de calificaciones
│   └── templates/
│       └── ratings/       # Plantillas HTML
│
├── reports/               # Aplicación de reportes
│   ├── models.py          # Reporte, HistorialEventos, ConfiguracionSistema
│   ├── views.py           # Vistas de admin y reportes
│   ├── urls.py            # Rutas de reportes
│   └── templates/
│       └── reports/       # Plantillas HTML
│
├── templates/             # Plantillas globales
│   ├── base.html          # Template base con Bootstrap
│   └── ...
│
├── static/                # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
│
├── manage.py              # Gestor de Django
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este archivo
```

##  Modelos de Datos

### Usuario
Usuario personalizado con campos adicionales para verificación, reputación y control de suspensiones.

### Vehículo
Registro de vehículos de conductores con información de marca, modelo, placa y capacidad.

### Viaje
Viajes publicados con información de origen, destino, horario y cupos disponibles.

### SolicitudViaje
Solicitudes de pasajeros para unirse a viajes específicos.

### Calificación
Sistema de reputación entre usuarios (Conductor ↔ Pasajero).

### Reporte
Reportes de conducta indebida con gestión administrativa.

### HistorialEventos
Trazabilidad completa de eventos del sistema.

### ConfiguracionSistema
Parámetros configurables del sistema (singleton).

##  Seguridad

-  Contraseñas hasheadas con PBKDF2
-  Verificación por correo institucional
-  CSRF protection
-  SQL Injection prevention (ORM)
-  Control de acceso basado en roles

##  Contacto y Soporte

Para reportar bugs o sugerencias, crear un issue en el repositorio.

**Última actualización:** Abril 2026
=======
**Acceso:**
- 🌐 Web: `http://localhost:8000`
- 👤 Admin: `http://localhost:8000/admin/`
- 📝 Registro: `http://localhost:8000/users/register/`

---

### Para WINDOWS: Usa [Docs/COMIENZA_AQUI_WINDOWS.md](Docs/COMIENZA_AQUI_WINDOWS.md)
Contiene soluciones para problemas comunes en Windows y guía detallada paso a paso.

##  Estructura del Proyecto

### 📁 Aplicaciones Django
- **users:** Autenticación, perfiles, vehículos
- **trips:** Publicación y búsqueda de viajes
- **ratings:** Calificaciones y reputación
- **reports:** Reportes y panel administrativo

### 🗄️ Modelos de Base de Datos

| Modelo | Descripción |
|--------|-------------|
| **Usuario** | Custom user con verificación, reputación, advertencias |
| **Vehículo** | Registro de vehículos de conductores |
| **Viaje** | Viajes publicados con cupos y estado |
| **SolicitudViaje** | Solicitudes de pasajeros a viajes |
| **Calificación** | Sistema de 5 estrellas entre usuarios |
| **Reporte** | Reportes de conducta indebida |
| **HistorialEventos** | Registro de trazabilidad |
| **ConfiguracionSistema** | Parámetros configurables |

## 📋 Funcionalidades Implementadas

✅ **Autenticación (RF1):** Registro y login con correo institucional + verificación por código  
✅ **Gestión de Perfil (RF2):** CRUD de datos personales y registro de vehículos  
✅ **Publicación de Viajes (RF3):** Formulario con origen, destino, fecha, cupos  
✅ **Búsqueda de Viajes (RF4):** Filtros por zona, fecha, hora  
✅ **Gestión de Solicitudes (RF5-RF6):** Aceptar/rechazar pasajeros  
✅ **Calificaciones (RF8):** Sistema de reseñas y calificación  
✅ **Reportes (RF11):** Reporte de conducta indebida  
✅ **Panel Admin:** Dashboard, gestión de usuarios y advertencias  
✅ **Seguridad:** Contraseñas hasheadas, CSRF protection, SQL injection prevention

## 🔒 Medidas de Seguridad

- ✅ Contraseñas hasheadas con PBKDF2
- ✅ Verificación por correo institucional (código de 6 dígitos)
- ✅ CSRF protection
- ✅ SQL Injection prevention (ORM)
- ✅ Control de acceso basado en roles
- ✅ Trazabilidad completa de eventos

## 📚 Documentación Adicional

- **[Docs/COMIENZA_AQUI_WINDOWS.md](Docs/COMIENZA_AQUI_WINDOWS.md)** - Guía detallada para Windows (instalación automática y manual)
- **[Docs/VERIFICACION_CORREO.md](Docs/VERIFICACION_CORREO.md)** - Documentación del sistema de verificación de correo institucional

## 📊 Estadísticas del Proyecto

- ✅ **24** archivos Python
- ✅ **16** templates HTML con Bootstrap 5
- ✅ **8** modelos de base de datos
- ✅ **20+** vistas implementadas
- ✅ **4,500+** líneas de código

## 👥 Roles del Sistema

1. **Estudiante (Pasajero):** Busca viajes, solicita unirse, califica conductores
2. **Estudiante (Conductor):** Publica viajes, acepta/rechaza pasajeros, califica
3. **Administrador:** Gestiona reportes, advertencias y suspensiones

## 🔗 URLs Principales

```
/                              # Página principal
/users/register/               # Registro de usuario
/users/login/                  # Login
/users/profile/                # Perfil del usuario
/trips/search/                 # Búsqueda de viajes
/trips/publish/                # Publicar viaje
/trips/my-trips/               # Mis viajes
/ratings/rate/                 # Calificar usuario
/reports/report-user/          # Reportar usuario
/admin/                        # Panel administrativo
```

## 📧 Verificación de Correo

El sistema usa un código de 6 dígitos único para verificar que el usuario pertenece a la institución.  
Más detalles en [Docs/VERIFICACION_CORREO.md](Docs/VERIFICACION_CORREO.md)

## 🤝 Soporte

Para reportar bugs o sugerencias, crear un issue en el repositorio.

**Última actualización:** Mayo 2026
>>>>>>> 5dab252 (Reorganizacion .md)
