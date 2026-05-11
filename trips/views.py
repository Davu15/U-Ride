from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from .models import Viaje, SolicitudViaje
from users.models import Vehiculo


@login_required(login_url='users:login')
def publish_trip(request):
    """Vista para publicar un nuevo viaje."""
    if request.method == 'POST':
        try:
            viaje = Viaje(
                conductor=request.user,
                zona_origen=request.POST.get('zona_origen'),
                zona_destino=request.POST.get('zona_destino'),
                fecha_hora_salida=request.POST.get('fecha_hora_salida'),
                cupos_totales=int(request.POST.get('cupos_totales')),
                cupos_disponibles=int(request.POST.get('cupos_totales')),
                notas_reglas=request.POST.get('notas_reglas', ''),
            )
            
            vehiculo_id = request.POST.get('vehiculo')
            if vehiculo_id:
                viaje.vehiculo = Vehiculo.objects.get(id=vehiculo_id, usuario=request.user)
            
            viaje.save()
            messages.success(request, 'Viaje publicado correctamente')
            return redirect('trips:my_trips')
        except Exception as e:
            messages.error(request, f'Error al publicar viaje: {str(e)}')
    
    vehiculos = request.user.vehiculos.filter(activo=True)
    context = {'vehiculos': vehiculos}
    return render(request, 'trips/publish_trip.html', context)


@login_required(login_url='users:login')
def my_trips(request):
    """Vista para ver los viajes del conductor."""
    viajes = request.user.viajes_como_conductor.all()
    context = {'viajes': viajes}
    return render(request, 'trips/my_trips.html', context)


@login_required(login_url='users:login')
def trip_requests(request, trip_id):
    """Vista para ver las solicitudes de un viaje."""
    viaje = get_object_or_404(Viaje, id=trip_id, conductor=request.user)
    solicitudes = viaje.solicitudes_pasajeros.all()
    context = {'viaje': viaje, 'solicitudes': solicitudes}
    return render(request, 'trips/trip_requests.html', context)


@login_required(login_url='users:login')
def accept_request(request, request_id):
    """Vista para aceptar una solicitud."""
    solicitud = get_object_or_404(SolicitudViaje, id=request_id)
    
    if solicitud.viaje.conductor != request.user:
        messages.error(request, 'No tienes permiso para aceptar esta solicitud')
        return redirect('trips:my_trips')
    
    if solicitud.viaje.cupos_disponibles > 0:
        solicitud.estado = 'Confirmada'
        solicitud.fecha_respuesta = timezone.now()
        solicitud.save()
        
        solicitud.viaje.cupos_disponibles -= 1
        solicitud.viaje.save()
        
        messages.success(request, 'Solicitud aceptada')
    else:
        messages.error(request, 'No hay cupos disponibles')
    
    return redirect('trips:trip_requests', trip_id=solicitud.viaje.id)


@login_required(login_url='users:login')
def reject_request(request, request_id):
    """Vista para rechazar una solicitud."""
    solicitud = get_object_or_404(SolicitudViaje, id=request_id)
    
    if solicitud.viaje.conductor != request.user:
        messages.error(request, 'No tienes permiso para rechazar esta solicitud')
        return redirect('trips:my_trips')
    
    solicitud.estado = 'Rechazada'
    solicitud.fecha_respuesta = timezone.now()
    solicitud.save()
    
    messages.success(request, 'Solicitud rechazada')
    return redirect('trips:trip_requests', trip_id=solicitud.viaje.id)


def search_trips(request):
    """Vista para buscar viajes disponibles."""
    viajes = Viaje.objects.filter(
        estado='Activo',
        cupos_disponibles__gt=0,
        fecha_hora_salida__gte=timezone.now()
    )
    
    # Filtros
    zona_origen = request.GET.get('zona_origen', '')
    zona_destino = request.GET.get('zona_destino', '')
    fecha = request.GET.get('fecha', '')
    
    if zona_origen:
        viajes = viajes.filter(zona_origen__icontains=zona_origen)
    if zona_destino:
        viajes = viajes.filter(zona_destino__icontains=zona_destino)
    if fecha:
        viajes = viajes.filter(fecha_hora_salida__date=fecha)
    
    context = {
        'viajes': viajes,
        'zona_origen': zona_origen,
        'zona_destino': zona_destino,
        'fecha': fecha,
    }
    return render(request, 'trips/search_trips.html', context)


def trip_detail(request, trip_id):
    """Vista para ver detalles de un viaje."""
    viaje = get_object_or_404(Viaje, id=trip_id)
    context = {'viaje': viaje}
    return render(request, 'trips/trip_detail.html', context)


@login_required(login_url='users:login')
def request_trip(request, trip_id):
    """Vista para solicitar un viaje."""
    viaje = get_object_or_404(Viaje, id=trip_id)
    
    # Verificar si el usuario ya tiene una solicitud para este viaje
    if SolicitudViaje.objects.filter(viaje=viaje, pasajero=request.user).exists():
        messages.warning(request, 'Ya has solicitado este viaje')
        return redirect('trips:trip_detail', trip_id=trip_id)
    
    try:
        solicitud = SolicitudViaje(viaje=viaje, pasajero=request.user)
        solicitud.save()
        messages.success(request, 'Solicitud enviada correctamente')
    except Exception as e:
        messages.error(request, f'Error al solicitar viaje: {str(e)}')
    
    return redirect('trips:trip_detail', trip_id=trip_id)
