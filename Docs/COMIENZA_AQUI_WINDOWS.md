# 🚀 GUÍA DE INSTALACIÓN - WINDOWS

U-Ride requiere Python, MySQL y algunas dependencias. Este archivo tiene los pasos exactos para Windows.

## ⚡ OPCIÓN 1: Instalación Automática (MÁS RÁPIDA)

Simplemente **haz doble clic en:**
```
setup_windows.bat
```

El script hace todo automáticamente:
- ✅ Crea entorno virtual
- ✅ Instala dependencias
- ✅ Crea archivo .env
- ✅ Ejecuta migraciones
- ✅ Crea superusuario
- ✅ Inicia servidor

**¡En 2 minutos estarás listo!** ⏱️

---

## ⚙️ OPCIÓN 2: Instalación Manual (Si algo falla)

### PASO 1: Abrir Terminal CMD

```cmd
Windows + R
Escribir: cmd
Presionar: Enter
```

Deberías estar en la carpeta del proyecto.

### PASO 2: Crear y Activar Entorno Virtual

```cmd
REM Crear entorno virtual
python -m venv venv

REM Activar entorno virtual
venv\Scripts\activate
```

**✅ Éxito:** Deberías ver `(venv)` al inicio de la línea:
```
(venv) C:\Users\WELCOME\Desktop\U-Ride>
```

**❌ Si no aparece (venv):** Intenta en PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### PASO 3: Instalar Dependencias

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

**Espera a que termine.** Debería ver:
```
Successfully installed Django-5.0.1 Pillow-11.0.0 python-dotenv-1.0.0 mysqlclient-2.2.6
```

### PASO 4: Verificar Django

```cmd
python -m django --version
```

Debería mostrar: `5.0.1` ✅

### PASO 5: Preparar Base de Datos MySQL

**A) Crear la base de datos:**

Opción A (MySQL desde CMD):
```cmd
mysql -u root -p
REM Ingresa tu contraseña de MySQL
```

Dentro de MySQL ejecuta:
```sql
CREATE DATABASE u_ride_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

Opción B (MySQL Workbench):
- Abre MySQL Workbench
- Clic en `+` para nueva conexión
- Ejecuta el comando anterior

**B) Copiar configuración de entorno:**

```cmd
REM Copiar archivo .env.example a .env
copy .env.example .env
```

**C) Editar .env:**

```cmd
REM Abrir con Bloc de Notas
notepad .env
```

Busca y edita estas líneas:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
DB_NAME=u_ride_db
DB_USER=root
DB_PASSWORD=TU_CONTRASEÑA_MYSQL_AQUI
DB_HOST=localhost
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
INSTITUTIONAL_EMAIL_DOMAIN=uta.edu.ec
```

Guarda: `Ctrl+S`

### PASO 6: Ejecutar Migraciones

```cmd
python manage.py makemigrations

REM Verifica que no haya errores, luego:
python manage.py migrate
```

### PASO 7: Crear Superusuario (Admin)

```cmd
python manage.py createsuperuser
```

Te pedirá:
- **Username:** (pulsa Enter para dejar en blanco)
- **Email:** `admin@uta.edu.ec`
- **Password:** (elige una contraseña segura)
- **Confirmar Password:** (repite)

### PASO 8: ¡Ejecutar Servidor!

```cmd
python manage.py runserver
```

Deberías ver:
```
Starting development server at http://127.0.0.1:8000/
```

Abre en el navegador: **http://localhost:8000**

---

## 🔗 Acceso a la Aplicación

| Sección | URL |
|---------|-----|
| 🏠 Página Principal | http://localhost:8000 |
| 📝 Registro | http://localhost:8000/users/register/ |
| 🔑 Login | http://localhost:8000/users/login/ |
| 👤 Admin Django | http://localhost:8000/admin/ |

---

## 🆘 Problemas Comunes y Soluciones

### ❌ Error: "venv\Scripts\activate no es reconocido"

**Solución 1 - PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**Solución 2 - Verificar Python:**
```cmd
python --version
```
Debe ser 3.8 o superior.

### ❌ Error: "ModuleNotFoundError: No module named 'django'"

**Causa:** El entorno virtual no está activo.

**Solución:**
```cmd
REM Verifica que veas (venv) al inicio de la línea
REM Si no, ejecuta:
venv\Scripts\activate

REM Luego instala de nuevo:
pip install -r requirements.txt
```

### ❌ Error: "Access denied" en MySQL

**Causa:** Contraseña incorrecta de MySQL.

**Solución:**
1. Abre `.env` con `notepad .env`
2. Verifica `DB_PASSWORD` (debe ser tu contraseña de MySQL)
3. Verifica `DB_USER` (generalmente es `root`)
4. Verifica `DB_HOST` (debe ser `localhost`)
5. Guarda y vuelve a ejecutar `python manage.py migrate`

### ❌ Error: "Port 8000 already in use"

**Causa:** Otro proceso está usando el puerto 8000.

**Solución:**
```cmd
REM Usa otro puerto
python manage.py runserver 8001
```

Accede a: **http://localhost:8001**

### ❌ Error: "django-admin: command not found"

**Causa:** Entorno virtual no activado.

**Solución:**
```cmd
venv\Scripts\activate
python -m django --version
```

### ❌ Error: "mysql-connector-python" install fails

**Solución:**
```cmd
pip install --upgrade pip setuptools wheel
pip install mysqlclient
```

---

## ✅ Checklist de Verificación

- [ ] Python 3.8+ instalado
- [ ] MySQL 5.7+ funcionando
- [ ] Entorno virtual creado y activado (ves `(venv)`)
- [ ] `pip install -r requirements.txt` sin errores
- [ ] `python -m django --version` muestra 5.0.1
- [ ] Base de datos `u_ride_db` creada
- [ ] `.env` configurado correctamente
- [ ] `python manage.py migrate` completado
- [ ] Superusuario creado
- [ ] Servidor corriendo en http://localhost:8000

---

## 💡 Resumen Rápido (Copiar y Pegar)

```cmd
REM 1. Activar entorno
venv\Scripts\activate

REM 2. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

REM 3. Copiar .env
copy .env.example .env

REM 4. Editar .env (cambiar DB_PASSWORD con tu contraseña)
notepad .env

REM 5. Migraciones
python manage.py makemigrations
python manage.py migrate

REM 6. Crear admin
python manage.py createsuperuser

REM 7. Ejecutar
python manage.py runserver
```

Accede a: **http://localhost:8000** ✅

---

## ⚠️ Importante

- **El entorno virtual DEBE estar activado** cada vez que trabajes
- Si cierras la terminal, al abrirla nuevamente ejecuta: `venv\Scripts\activate`
- El archivo `.env` **NUNCA** debe commitirse a git (ya está en .gitignore)
- Para detener el servidor: `Ctrl+C`

---

## 📚 Más Información

- [README.md](README.md) - Documentación general del proyecto
- [VERIFICACION_CORREO.md](VERIFICACION_CORREO.md) - Sistema de verificación de correo

