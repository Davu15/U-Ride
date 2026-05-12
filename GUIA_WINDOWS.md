# GUÍA PARA WINDOWS - U-Ride

## ⚠️ IMPORTANTE: Sigue estos pasos EXACTAMENTE para Windows

### PASO 1: Crear Entorno Virtual (OBLIGATORIO)

```cmd
REM Crear entorno virtual
python -m venv venv

REM Activar entorno virtual
venv\Scripts\activate

REM Deberías ver: (venv) C:\Users\WELCOME\Desktop\U-Ride>
```

**¿No aparece (venv)?** Intenta en PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### PASO 2: Instalar Dependencias (Ahora va a funcionar)

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

**Espera a que termine sin errores.** Debería ver:
```
Successfully installed Django-5.0.1 Pillow-11.0.0 python-dotenv-1.0.0 mysqlclient-2.2.6
```

### PASO 3: Verificar que Django está instalado

```cmd
python -m django --version
```

Debería mostrar: `5.0.1`

---

## PASO 4: Configurar Base de Datos MySQL

### 4.1 Crear la base de datos

**Opción A: Usar MySQL desde CMD**

```cmd
REM Abre conexión a MySQL (ingresa contraseña)
mysql -u root -p

REM Una vez dentro de MySQL, ejecuta:
CREATE DATABASE u_ride_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

**Opción B: Usar MySQL Workbench**
- Abre MySQL Workbench
- Clic en "+" para crear nueva conexión
- Ejecuta: `CREATE DATABASE u_ride_db CHARACTER SET utf8mb4;`

### 4.2 Copiar archivo .env

```cmd
REM En Windows, usar copy en lugar de cp
copy .env.example .env
```

### 4.3 Editar .env

```cmd
REM Abrir .env con bloc de notas
notepad .env
```

**Cambiar estas líneas:**

```env
DB_PASSWORD=TU_CONTRASEÑA_MYSQL_AQUI
```

Guarda el archivo (Ctrl+S)

---

## PASO 5: Ejecutar Migraciones

```cmd
python manage.py makemigrations

REM Verifica que no haya errores, luego:
python manage.py migrate
```

---

## PASO 6: Crear Superusuario (Admin)

```cmd
python manage.py createsuperuser
```

**Te pedirá:**
- Username: (pulsa Enter para dejar en blanco)
- Email: `admin@uta.edu.ec`
- Password: (tu contraseña)
- Confirmar: (repite contraseña)

---

## PASO 7: ¡Ejecutar el Servidor!

```cmd
python manage.py runserver
```

**Verás:**
```
Starting development server at http://127.0.0.1:8000/
```

Abre navegador: http://localhost:8000

---

## 🆘 Si algo falla...

### Error: "venv\Scripts\activate no es reconocido"

```cmd
REM En PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Error: "ModuleNotFoundError: No module named 'django'"

Verifica que el entorno esté activo:
```cmd
REM Debe verse: (venv) C:\Users\WELCOME\Desktop\U-Ride>
```

Si no, ejecuta:
```cmd
venv\Scripts\activate
```

### Error: "Access denied" en MySQL

Usa contraseña correcta en .env:
```env
DB_PASSWORD=tu_contraseña_mysql_aqui
DB_HOST=localhost
DB_USER=root
```

### Error: "Port 8000 already in use"

Usa otro puerto:
```cmd
python manage.py runserver 8001
```

---

## ✅ Checklist Final

- [ ] Entorno virtual creado y activado
- [ ] `pip install -r requirements.txt` completado sin errores
- [ ] `django-admin --version` muestra 5.0.1
- [ ] Base de datos `u_ride_db` creada
- [ ] `.env` configurado con contraseña MySQL
- [ ] `python manage.py migrate` sin errores
- [ ] Superusuario creado
- [ ] Servidor corriendo en http://localhost:8000

---

## 📝 Acceso a la Aplicación

### Registro de Nuevo Usuario
http://localhost:8000/users/register/

### Login
http://localhost:8000/users/login/

### Panel de Admin Django
http://localhost:8000/admin/
- Email: admin@uta.edu.ec
- Password: (la que ingresaste)

---

## ⚡ Resumen Rápido (copiar y pegar)

```cmd
REM 1. Activar entorno
venv\Scripts\activate

REM 2. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

REM 3. Copiar .env
copy .env.example .env

REM 4. Editar .env (cambiar DB_PASSWORD)
notepad .env

REM 5. Migraciones
python manage.py makemigrations
python manage.py migrate

REM 6. Crear admin
python manage.py createsuperuser

REM 7. Ejecutar
python manage.py runserver
```

¡Listo! Accede a http://localhost:8000

---

**Nota:** El entorno virtual DEBE estar activo cada vez que trabajes. Si cierras la terminal y la abres de nuevo, ejecuta:
```cmd
venv\Scripts\activate
```

