# 🚀 COMIENZA AQUÍ - WINDOWS

## ⚡ Opción 1: Instalación Automática (RECOMENDADO)

Simplemente **haz doble clic** en:
```
setup_windows.bat
```

El script hará todo automáticamente:
- ✅ Crear entorno virtual
- ✅ Instalar dependencias
- ✅ Crear archivo .env
- ✅ Ejecutar migraciones
- ✅ Crear superusuario
- ✅ Iniciar servidor

---

## ⚙️ Opción 2: Instalación Manual (Si algo falla)

### Paso 1: Abrir Cmd en la carpeta del proyecto
```
Windows + R → cmd → Enter
```

### Paso 2: Crear y Activar Entorno Virtual
```cmd
python -m venv venv
venv\Scripts\activate
```

Deberías ver: `(venv) C:\Users\WELCOME\Desktop\U-Ride>`

### Paso 3: Instalar Dependencias
```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

Espera a que termine sin errores.

### Paso 4: Copiar Configuración
```cmd
copy .env.example .env
```

### Paso 5: Editar .env
```cmd
notepad .env
```

Encuentra esta línea y escribe tu contraseña de MySQL:
```
DB_PASSWORD=TU_CONTRASEÑA_AQUI
```

Guarda (Ctrl+S) y cierra.

### Paso 6: Crear Base de Datos MySQL
Abre MySQL Workbench o MySQL Command Line y ejecuta:
```sql
CREATE DATABASE u_ride_db CHARACTER SET utf8mb4;
```

### Paso 7: Migraciones
```cmd
python manage.py migrate
```

### Paso 8: Crear Admin
```cmd
python manage.py createsuperuser
```

Email: `admin@estudiantes.ucentral.edu.co`
Contraseña: (elige una)

### Paso 9: ¡Ejecutar!
```cmd
python manage.py runserver
```

Abre: **http://localhost:8000**

---

## 🔗 Acceso

- **Web:** http://localhost:8000
- **Admin:** http://localhost:8000/admin/
- **Registro:** http://localhost:8000/users/register/

---

## ❓ Problemas Comunes

### Error: "venv no se reconoce"
```cmd
REM Prueba en PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Error: "ModuleNotFoundError: No module named 'django'"
Verifica que el entorno esté activo (debe verse `(venv)`)

### Error: "Access denied" en MySQL
Verifica la contraseña en `.env`

### Error: "Port 8000 already in use"
```cmd
python manage.py runserver 8001
```

---

## 📚 Documentación Completa

- **GUIA_WINDOWS.md** - Guía detallada para Windows
- **README.md** - Documentación del proyecto
- **ESTRUCTURA_VERIFICACION.md** - Checklist de archivos

---

¡**Eso es todo!** Si usas el script automático, ¡en 2 minutos estarás listo! ⏱️

