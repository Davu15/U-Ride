from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Reporte, HistorialEventos, ConfiguracionSistema
from trips.models import Viaje
from users.models import Usuario


@login_required(login_url='users:login')
def report_user(request, trip_id):
    """Vista para reportar conducta indebida."""
    viaje = get_object_or_404(Viaje, id=trip_id)
    
    # Determinar contra quién se puede reportar
    usuario_a_reportar = None
    if viaje.conductor == request.user:
        # Si soy el conductor, puedo reportar a los pasajeros confirmados
        pass
    else:
        # Si soy pasajero, puedo reportar al conductor
        usuario_a_reportar = viaje.conductor
    
    if request.method == 'POST':
        try:
            usuario_reportado_id = request.POST.get('usuario_reportado')
            usuario_reportado = Usuario.objects.get(id=usuario_reportado_id)
            
            # Verificar permisos
            if viaje.conductor == request.user:
                # El conductor puede reportar pasajeros de su viaje
                pass
            elif usuario_reportado == viaje.conductor:
                # El pasajero puede reportar solo al conductor
                pass
            else:
                messages.error(request, 'No tienes permiso para reportar a este usuario')
                return redirect('trips:trip_detail', trip_id=trip_id)
            
            # Crear reporte
            reporte = Reporte(
                reportador=request.user,
                reportado=usuario_reportado,
                viaje=viaje,
                motivo=request.POST.get('motivo'),
                descripcion=request.POST.get('descripcion'),
            )
            reporte.save()
            
            # Registrar en historial
            HistorialEventos.objects.create(
                tipo_evento='Reporte',
                usuario=request.user,
                descripcion=f'Reporte contra {usuario_reportado.correo_institucional}',
                detalles={'reporte_id': reporte.id, 'viaje_id': viaje.id}
            )
            
            messages.success(request, 'Reporte enviado correctamente')
            return redirect('trips:trip_detail', trip_id=trip_id)
        except Exception as e:
            messages.error(request, f'Error al crear reporte: {str(e)}')
    
    context = {
        'viaje': viaje,
        'usuario_a_reportar': usuario_a_reportar,
    }
    return render(request, 'reports/report_user.html', context)


def is_admin(user):
    """Verifica si el usuario es administrador."""
    return user.is_staff or user.is_superuser


@user_passes_test(is_admin, login_url='users:login')
def admin_dashboard(request):
    """Dashboard del administrador."""
    # Estadísticas
    total_usuarios = Usuario.objects.count()
    usuarios_verificados = Usuario.objects.filter(verificado=True).count()
    total_viajes = Viaje.objects.count()
    viajes_activos = Viaje.objects.filter(estado='Activo').count()
    
    # Reportes pendientes
    reportes_pendientes = Reporte.objects.filter(estado='Pendiente').count()
    
    # Usuarios con problemas
    usuarios_con_advertencias = Usuario.objects.filter(advertencias__gt=0)
    usuarios_suspendidos = Usuario.objects.filter(suspendido_hasta__isnull=False)
    
    context = {
        'total_usuarios': total_usuarios,
        'usuarios_verificados': usuarios_verificados,
        'total_viajes': total_viajes,
        'viajes_activos': viajes_activos,
        'reportes_pendientes': reportes_pendientes,
        'usuarios_con_advertencias': usuarios_con_advertencias,
        'usuarios_suspendidos': usuarios_suspendidos,
    }
    return render(request, 'reports/admin_dashboard.html', context)


@user_passes_test(is_admin, login_url='users:login')
def review_report(request, report_id):
    """Vista para revisar un reporte."""
    reporte = get_object_or_404(Reporte, id=report_id)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        descripcion = request.POST.get('descripcion')
        
        reporte.estado = 'Resuelto'
        reporte.revisado_por = request.user
        reporte.fecha_revision = timezone.now()
        reporte.accion_tomada = descripcion
        reporte.save()
        
        # Aplicar acción
        config = ConfiguracionSistema.get_configuracion()
        
        if accion == 'advertencia':
            reporte.reportado.advertencias += 1
            reporte.reportado.save()
            
            HistorialEventos.objects.create(
                tipo_evento='Advertencia',
                usuario=reporte.reportado,
                descripcion=f'Advertencia por reporte: {reporte.motivo}',
                detalles={'reporte_id': reporte.id}
            )
            
            # Verificar si debe ser suspendido
            if reporte.reportado.advertencias >= config.limite_advertencias:
                dias = reporte.reportado.advertencias * config.dias_suspension
                reporte.reportado.suspendido_hasta = timezone.now() + timedelta(days=dias)
                reporte.reportado.save()
                
                HistorialEventos.objects.create(
                    tipo_evento='Suspensión',
                    usuario=reporte.reportado,
                    descripcion=f'Suspendido por {dias} días',
                    detalles={'reporte_id': reporte.id}
                )
                
                messages.success(request, f'Usuario advertido y suspendido por {dias} días')
            else:
                messages.success(request, 'Usuario advertido')
        
        elif accion == 'suspender':
            dias = int(request.POST.get('dias_suspension', 7))
            reporte.reportado.suspendido_hasta = timezone.now() + timedelta(days=dias)
            reporte.reportado.save()
            
            HistorialEventos.objects.create(
                tipo_evento='Suspensión',
                usuario=reporte.reportado,
                descripcion=f'Suspendido por {dias} días',
                detalles={'reporte_id': reporte.id}
            )
            
            messages.success(request, f'Usuario suspendido por {dias} días')
        
        return redirect('reports:admin_dashboard')
    
    context = {'reporte': reporte}
    return render(request, 'reports/review_report.html', context)


@user_passes_test(is_admin, login_url='users:login')
def manage_users(request):
    """Vista para gestionar usuarios."""
    usuarios = Usuario.objects.all()
    
    # Filtros
    filtro = request.GET.get('filtro', '')
    if filtro == 'advertencias':
        usuarios = usuarios.filter(advertencias__gt=0)
    elif filtro == 'suspendidos':
        usuarios = usuarios.filter(suspendido_hasta__isnull=False)
    
    context = {'usuarios': usuarios, 'filtro': filtro}
    return render(request, 'reports/manage_users.html', context)
