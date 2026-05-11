from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError

from .models import Usuario, Vehiculo
from .forms import (
    RegistroUsuarioForm, VerificacionCodigoForm, LoginUsuarioForm,
    SolicitarRecuperacionForm, VerificacionCodigoRecuperacionForm,
    CambiarContraseñaRecuperacionForm
)
from .services import (
    generar_y_enviar_codigo, verificar_usuario, enviar_codigo_reintento,
    generar_y_enviar_codigo_recuperacion, verificar_codigo_recuperacion,
    cambiar_contrasena_recuperacion
)


@require_http_methods(["GET", "POST"])
def register(request):
    """
    Vista para el registro de nuevos usuarios con validación de dominio institucional.
    """
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        
        if form.is_valid():
            try:
                usuario = form.save()
                
                # Generar y enviar código de verificación
                success, mensaje = generar_y_enviar_codigo(usuario)
                
                if success:
                    messages.success(
                        request,
                        f'¡Registro exitoso! Verifica tu correo en {usuario.correo_institucional} para activar tu cuenta.'
                    )
                    request.session['correo_registrado'] = usuario.correo_institucional
                    return redirect('users:verify_email')
                else:
                    usuario.delete()
                    messages.error(request, f'Error al enviar código: {mensaje}')
            
            except IntegrityError:
                messages.error(request, 'Este correo ya está registrado en el sistema')
            except Exception as e:
                messages.error(request, f'Error inesperado: {str(e)}')
        
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
    else:
        form = RegistroUsuarioForm()
    
    context = {
        'form': form,
        'titulo': 'Registro',
        'subtitulo': 'Crear nueva cuenta',
    }
    
    return render(request, 'users/register.html', context)


@require_http_methods(["GET", "POST"])
def verify_email(request):
    """
    Vista para verificar el correo mediante código de 6 dígitos.
    """
    if request.user.is_authenticated and request.user.verificado:
        return redirect('users:profile')
    
    # Obtener correo de sesión si existe
    correo_sesion = request.session.get('correo_registrado', '')
    
    if request.method == 'POST':
        form = VerificacionCodigoForm(request.POST)
        
        if form.is_valid():
            correo = form.cleaned_data['correo_institucional'].lower()
            codigo = form.cleaned_data['codigo']
            
            # Usar servicio de verificación
            success, usuario, mensaje = verificar_usuario(correo, codigo)
            
            if success:
                messages.success(request, '✅ ' + mensaje + ' Ahora puedes iniciar sesión.')
                request.session.pop('correo_registrado', None)
                return redirect('users:login')
            else:
                messages.error(request, '❌ ' + mensaje)
        
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, str(error))
    
    else:
        form = VerificacionCodigoForm(initial={'correo_institucional': correo_sesion})
    
    context = {
        'form': form,
        'correo_registrado': correo_sesion,
        'titulo': 'Verificar Correo',
        'subtitulo': 'Ingresa el código que recibiste',
    }
    
    return render(request, 'users/verify_email.html', context)


@require_http_methods(["POST"])
def reenviar_codigo(request):
    """
    Vista para reenviar el código de verificación.
    """
    correo = request.POST.get('correo_institucional', '').lower()
    
    if not correo:
        messages.error(request, 'Ingresa tu correo institucional')
        return redirect('users:verify_email')
    
    success, mensaje = enviar_codigo_reintento(correo)
    
    if success:
        messages.success(request, f'✉️ ' + mensaje)
    else:
        messages.error(request, '❌ ' + mensaje)
    
    return redirect('users:verify_email')


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Vista para login usando correo institucional.
    Valida que el usuario esté verificado.
    """
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = LoginUsuarioForm(request.POST)
        
        if form.is_valid():
            correo = form.cleaned_data['correo_institucional']
            password = form.cleaned_data['password']
            
            try:
                usuario = Usuario.objects.get(correo_institucional=correo)
                
                # Validar que esté verificado
                if not usuario.verificado:
                    messages.error(request, '⚠️ Tu correo no está verificado. Completa la verificación primero.')
                    return redirect('users:verify_email')
                
                # Validar que no esté suspendido
                if usuario.esta_suspendido():
                    messages.error(request, f'❌ Tu cuenta está suspendida hasta {usuario.suspendido_hasta}')
                    return redirect('users:login')
                
                # Autenticar
                user = authenticate(request, username=usuario.username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, f'¡Bienvenido {user.get_full_name()}!')
                    return redirect('users:profile')
                else:
                    messages.error(request, '❌ Correo o contraseña incorrectos')
            
            except Usuario.DoesNotExist:
                messages.error(request, '❌ Usuario no encontrado')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, str(error))
    
    else:
        form = LoginUsuarioForm()
    
    context = {
        'form': form,
        'titulo': 'Iniciar Sesión',
        'subtitulo': 'Accede a tu cuenta',
    }
    
    return render(request, 'users/login.html', context)


@require_http_methods(["GET"])
@login_required(login_url='users:login')
def logout_view(request):
    """
    Vista para cerrar sesión.
    """
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('users:login')


# ============================================================================
# VISTAS DE RECUPERACIÓN DE CONTRASEÑA
# ============================================================================

@require_http_methods(["GET", "POST"])
def forgot_password(request):
    """
    Vista para solicitar la recuperación de contraseña.
    El usuario ingresa su correo institucional.
    """
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = SolicitarRecuperacionForm(request.POST)
        
        if form.is_valid():
            correo = form.cleaned_data['correo_institucional']
            
            # Generar y enviar código
            success, mensaje = generar_y_enviar_codigo_recuperacion(correo)
            
            if success:
                messages.success(
                    request,
                    f'✉️ {mensaje} Revisa tu correo para obtener el código.'
                )
                request.session['correo_recuperacion'] = correo
                return redirect('users:verify_reset_code')
            else:
                messages.error(request, f'❌ {mensaje}')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, str(error))
    
    else:
        form = SolicitarRecuperacionForm()
    
    context = {
        'form': form,
        'titulo': '¿Olvidaste tu Contraseña?',
        'subtitulo': 'Ingresa tu correo para recuperarla',
    }
    
    return render(request, 'users/forgot_password.html', context)


@require_http_methods(["GET", "POST"])
def verify_reset_code(request):
    """
    Vista para verificar el código de recuperación.
    """
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    # Obtener correo de sesión
    correo_sesion = request.session.get('correo_recuperacion', '')
    
    if not correo_sesion:
        messages.warning(request, 'Primero debes solicitar la recuperación de contraseña')
        return redirect('users:forgot_password')
    
    if request.method == 'POST':
        form = VerificacionCodigoRecuperacionForm(request.POST)
        
        if form.is_valid():
            correo = form.cleaned_data['correo_institucional'].lower()
            codigo = form.cleaned_data['codigo']
            
            # Verificar código
            success, mensaje = verificar_codigo_recuperacion(correo, codigo)
            
            if success:
                messages.success(request, f'✅ {mensaje} Ahora puedes cambiar tu contraseña.')
                return redirect('users:reset_password')
            else:
                messages.error(request, f'❌ {mensaje}')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, str(error))
    
    else:
        form = VerificacionCodigoRecuperacionForm(
            initial={'correo_institucional': correo_sesion}
        )
    
    context = {
        'form': form,
        'correo_recuperacion': correo_sesion,
        'titulo': 'Verificar Código',
        'subtitulo': 'Ingresa el código que recibiste por email',
    }
    
    return render(request, 'users/verify_reset_code.html', context)


@require_http_methods(["GET", "POST"])
def reset_password(request):
    """
    Vista para cambiar la contraseña.
    """
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    # Obtener correo de sesión
    correo_sesion = request.session.get('correo_recuperacion', '')
    
    if not correo_sesion:
        messages.warning(request, 'Debes verificar el código primero')
        return redirect('users:forgot_password')
    
    # Verificar que el usuario aún tiene un código válido
    try:
        usuario = Usuario.objects.get(correo_institucional=correo_sesion)
        if not usuario.codigo_recuperacion_valido():
            messages.error(request, 'El código de recuperación ha expirado. Solicita uno nuevo.')
            request.session.pop('correo_recuperacion', None)
            return redirect('users:forgot_password')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        request.session.pop('correo_recuperacion', None)
        return redirect('users:forgot_password')
    
    if request.method == 'POST':
        form = CambiarContraseñaRecuperacionForm(request.POST)
        
        if form.is_valid():
            correo = form.cleaned_data['correo_institucional'].lower()
            nueva_contrasena = form.cleaned_data['nueva_contrasena']
            
            # Cambiar contraseña
            success, mensaje = cambiar_contrasena_recuperacion(correo, nueva_contrasena)
            
            if success:
                messages.success(
                    request,
                    f'✅ {mensaje} Ya puedes iniciar sesión con tu nueva contraseña.'
                )
                request.session.pop('correo_recuperacion', None)
                return redirect('users:login')
            else:
                messages.error(request, f'❌ {mensaje}')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, str(error))
    
    else:
        form = CambiarContraseñaRecuperacionForm(
            initial={'correo_institucional': correo_sesion}
        )
    
    context = {
        'form': form,
        'correo_recuperacion': correo_sesion,
        'titulo': 'Cambiar Contraseña',
        'subtitulo': 'Crea una nueva contraseña segura',
    }
    
    return render(request, 'users/reset_password.html', context)


@require_http_methods(["GET"])
@login_required(login_url='users:login')
def profile(request):
    """
    Vista para mostrar el perfil del usuario.
    Valida que el usuario puede usar la plataforma.
    """
    usuario = request.user
    
    # Validar que puede usar plataforma
    if not usuario.puede_usar_plataforma():
        messages.warning(request, 'Tu cuenta no está completamente activa')
    
    vehiculos = usuario.vehiculos.filter(activo=True)
    
    context = {
        'usuario': usuario,
        'vehiculos': vehiculos,
        'titulo': 'Mi Perfil',
    }
    
    return render(request, 'users/profile.html', context)


@require_http_methods(["GET", "POST"])
@login_required(login_url='users:login')
def edit_profile(request):
    """
    Vista para editar el perfil del usuario.
    """
    usuario = request.user
    
    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name', usuario.first_name)
        usuario.last_name = request.POST.get('last_name', usuario.last_name)
        usuario.carrera = request.POST.get('carrera', usuario.carrera)
        usuario.numero_contacto = request.POST.get('numero_contacto', usuario.numero_contacto)
        usuario.zona_referencia = request.POST.get('zona_referencia', usuario.zona_referencia)
        
        if 'foto_perfil' in request.FILES:
            usuario.foto_perfil = request.FILES['foto_perfil']
        
        usuario.save()
        messages.success(request, 'Perfil actualizado exitosamente')
        return redirect('users:profile')
    
    context = {
        'usuario': usuario,
        'titulo': 'Editar Perfil',
    }
    
    return render(request, 'users/edit_profile.html', context)


@require_http_methods(["GET", "POST"])
@login_required(login_url='users:login')
def register_vehicle(request):
    """
    Vista para registrar un nuevo vehículo.
    """
    usuario = request.user
    
    if request.method == 'POST':
        try:
            vehiculo = Vehiculo.objects.create(
                usuario=usuario,
                marca=request.POST.get('marca'),
                modelo=request.POST.get('modelo'),
                ano=int(request.POST.get('ano')),
                color=request.POST.get('color'),
                placa=request.POST.get('placa').upper(),
                capacidad_asientos=int(request.POST.get('capacidad_asientos')),
            )
            messages.success(request, f'Vehículo {vehiculo.marca} {vehiculo.modelo} registrado exitosamente')
            return redirect('users:profile')
        
        except IntegrityError:
            messages.error(request, 'Esta placa ya está registrada')
        except (ValueError, KeyError) as e:
            messages.error(request, f'Error en los datos: {str(e)}')
    
    context = {
        'titulo': 'Registrar Vehículo',
        'subtitulo': 'Agrega un nuevo vehículo a tu perfil',
    }
    
    return render(request, 'users/register_vehicle.html', context)



#        usuario.save()
#        messages.success(request, 'Perfil actualizado correctamente')
#        return redirect('users:profile')
#
#    context = {'usuario': usuario}
#    return render(request, 'users/edit_profile.html', context)
#
#
# @login_required(login_url='users:login')
# def register_vehicle(request):
#     """Vista para registrar un vehículo."""
#     if request.method == 'POST':
#         try:
#             vehiculo = Vehiculo(
#                 usuario=request.user,
#                 marca=request.POST.get('marca'),
#                 modelo=request.POST.get('modelo'),
#                 ano=int(request.POST.get('ano')),
#                 color=request.POST.get('color'),
#                 placa=request.POST.get('placa').upper(),
#                 capacidad_asientos=int(request.POST.get('capacidad_asientos')),
#             )
#             vehiculo.full_clean()
#             vehiculo.save()
#             messages.success(request, 'Vehículo registrado correctamente')
#             return redirect('users:profile')
#         except Exception as e:
#             messages.error(request, f'Error al registrar vehículo: {str(e)}')
#
#     context = {}
#     return render(request, 'users/register_vehicle.html', context)