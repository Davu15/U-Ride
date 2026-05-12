# Guía de Inicio Rápido - U-Ride

## ⚠️ SI USAS WINDOWS

**Lee primero:** [`GUIA_WINDOWS.md`](GUIA_WINDOWS.md) - Tiene comandos específicos para Windows con soluciones para errores comunes

## Requisitos Previos
- Python 3.8 o superior
- MySQL 5.7 o superior
- pip
- Git (opcional)
- **IMPORTANTE EN WINDOWS:** Entorno virtual Python (venv)

## Pasos de Instalación

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Crear Base de Datos MySQL
```sql
-- Abre MySQL y ejecuta:
CREATE DATABASE u_ride_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configurar Variables de Entorno
```bash
# Copia el archivo .env.example a .env
cp .env.example .env

# Edita .env con tus valores:
# - Cambia DB_PASSWORD con tu contraseña de MySQL
# - Cambia SECRET_KEY con una clave segura
# - Configura EMAIL para enviar códigos de verificación
# - Cambia INSTITUTIONAL_EMAIL_DOMAIN si es necesario
```

### 4. Ejecutar Migraciones
```bash
# Aplicar todas las migraciones
python manage.py migrate

# Si hay problemas, crear migraciones manualmente:
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear Superusuario (Administrador)
```bash
python manage.py createsuperuser

# Se te pedirá que ingreses:
# - Username (puedes dejarlo en blanco)
# - Email (usa formato: admin@uta.edu.ec)
# - Password
# - Confirmar Password
```

### 6. Crear Datos de Prueba (Opcional)
```bash
python manage.py shell

# En la consola Python:
from django.contrib.auth import get_user_model
Usuario = get_user_model()

# Crear usuario de prueba
usuario_test = Usuario.objects.create_user(
    username='estudiante1',
    correo_institucional='estudiante1@uta.edu.ec',
    email='estudiante1@uta.edu.ec',
    password='TestPassword123!',
    first_name='Juan',
    last_name='Pérez',
    carrera='Ingeniería de Sistemas',
    verified=True  # Verificado automáticamente
)

# Salir
exit()
```

### 7. Iniciar Servidor de Desarrollo
```bash
python manage.py runserver

# El servidor estará disponible en:
# http://localhost:8000
```

## Acceso a la Aplicación

### Página Principal
- **URL:** http://localhost:8000
- **Redirección:** Te redirigirá a login si no estás autenticado

### Registro de Usuarios
- **URL:** http://localhost:8000/users/register/
- **Requisito:** Email con dominio institucional

### Login
- **URL:** http://localhost:8000/users/login/
- **Credencial:** Correo institucional + Contraseña

### Panel de Administración Django
- **URL:** http://localhost:8000/admin/
- **Credenciales:** Superusuario creado

### Panel de Administración U-Ride
- **URL:** http://localhost:8000/reports/dashboard/
- **Requisito:** Ser superusuario

## Flujos Principales

### 1. Registro e Verificación
1. Ir a `/users/register/`
2. Llenar formulario con correo institucional
3. Ir a `/users/verify-email/` e ingresar código
4. Hacer login

### 2. Registrar Vehículo (Conductor)
1. Ir a `/users/profile/`
2. Click en "Registrar Vehículo"
3. Llenar datos del vehículo

### 3. Publicar Viaje
1. Ir a `/trips/publish/`
2. Llenar detalles del viaje (origen, destino, hora, cupos)
3. Seleccionar vehículo
4. Publicar

### 4. Buscar y Solicitar Viaje
1. Ir a `/trips/search/`
2. Usar filtros para buscar viajes
3. Click "Ver Detalles"
4. Click "Solicitar Unirse"

### 5. Aceptar/Rechazar Solicitudes
1. Ir a `/trips/my-trips/`
2. Click en viaje para ver solicitudes
3. Aceptar o rechazar pasajeros

### 6. Calificar Usuarios
1. Ir a `/ratings/trip/<id>/rate/`
2. Calificar con estrellas y comentario
3. Enviar calificación

### 7. Reportar Conducta Indebida
1. Ir a `/reports/trip/<id>/report/`
2. Seleccionar motivo y describir incidente
3. Enviar reporte

## Solución de Problemas

### Error: "No such table: users_usuario"
**Solución:** Ejecutar migraciones
```bash
python manage.py migrate
```

### Error: "Access denied for user 'root'"
**Solución:** Verificar contraseña MySQL en `.env`
```env
DB_PASSWORD=tu_contraseña_correcta
```

### No puedo registrarme
**Solución:** Verificar que el dominio de email sea correcto
```env
INSTITUTIONAL_EMAIL_DOMAIN=uta.edu.ec
```

### Mensajes de email no se envían
**Solución:** Verificar configuración EMAIL en `.env`
```env
# Para desarrollo, puedes usar:
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Puerto 8000 ya está en uso
**Solución:** Usar otro puerto
```bash
python manage.py runserver 8001
```

## Estructura de Directorios Generada

```
U-Ride/
├── u_ride/                 # Config principal
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
├── users/                  # App de usuarios
├── trips/                  # App de viajes
├── ratings/                # App de calificaciones
├── reports/                # App de reportes
├── templates/              # Templates HTML
├── static/                 # Archivos estáticos
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## Próximos Pasos

1. **Personalizacion de emails:** Configurar templates de correo
2. **Estilos CSS:** Añadir estilos personalizados en `static/css/`
3. **Seguridad en Producción:**
   - Cambiar `DEBUG=False` en settings
   - Usar SECRET_KEY segura
   - Configurar ALLOWED_HOSTS
   - Usar base de datos productiva
4. **Desplegar:** Usar servidor web (Nginx, Apache) con Gunicorn

## Contacto y Soporte

Para más información o reportar problemas, revisa el README.md o contacta al equipo de desarrollo.

---

**Última actualización:** Abril 2026
