# README del Proyecto U-Ride

## 📱 Plataforma de Carpooling Seguro para Estudiantes

U-Ride es una plataforma web diseñada para facilitar el transporte compartido seguro entre estudiantes de una misma institución.

## 🚀 Características Principales

✅ **Autenticación Segura:** Acceso únicamente con correo institucional verificado
✅ **Gestión de Viajes:** Publicar, buscar y solicitar viajes
✅ **Sistema de Reputación:** Calificaciones y reseñas entre usuarios
✅ **Seguridad:** Reportes y gestión administrativa de incidentes
✅ **Trazabilidad:** Historial completo de eventos del sistema

## 🛠️ Stack Tecnológico

- **Backend:** Django 5.0
- **Frontend:** HTML5, CSS3, Bootstrap 5 (CDN)
- **Base de Datos:** MySQL
- **Autenticación:** Django Auth + Custom User Model

## 📋 Requisitos Previos

- Python 3.8+
- MySQL 5.7+
- pip

## 🔧 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <tu-repositorio>
cd U-Ride
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos MySQL
```sql
CREATE DATABASE u_ride_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurar Variablesd de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
DB_NAME=u_ride_db
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
INSTITUTIONAL_EMAIL_DOMAIN=estudiantes.ucentral.edu.co
```

### 6. Aplicar Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear Superusuario
```bash
python manage.py createsuperuser
```

### 8. Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```

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

## 🧪 Modelos de Datos

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

## 🔐 Seguridad

- ✅ Contraseñas hasheadas con PBKDF2
- ✅ Verificación por correo institucional
- ✅ CSRF protection
- ✅ SQL Injection prevention (ORM)
- ✅ Control de acceso basado en roles

## 📞 Contacto y Soporte

Para reportar bugs o sugerencias, crear un issue en el repositorio.

## 📄 Licencia

Proyecto educativo. Todos los derechos reservados.

---

**Última actualización:** Abril 2026
