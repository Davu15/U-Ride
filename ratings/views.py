from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Calificacion
from trips.models import Viaje, SolicitudViaje


@login_required(login_url='users:login')
def rate_users(request, trip_id):
    """Vista para calificar usuarios después de un viaje."""
    viaje = get_object_or_404(Viaje, id=trip_id)
    
    # Verificar permisos
    es_conductor = viaje.conductor == request.user
    solicitud = SolicitudViaje.objects.filter(
        viaje=viaje,
        pasajero=request.user,
        estado='Confirmada'
    ).first()
    es_pasajero = solicitud is not None
    
    if not (es_conductor or es_pasajero):
        messages.error(request, 'No participaste en este viaje')
        return redirect('trips:search_trips')
    
    if request.method == 'POST':
        try:
            if es_conductor:
                # Conductor califica a pasajeros
                for field_key in request.POST:
                    if field_key.startswith('pasajero_'):
                        pasajero_id = field_key.replace('pasajero_', '')
                        puntuacion = int(request.POST.get(field_key, 0))
                        resena = request.POST.get(f'resena_{pasajero_id}', '')
                        
                        if 1 <= puntuacion <= 5:
                            calificacion, _ = Calificacion.objects.get_or_create(
                                viaje=viaje,
                                evaluador=request.user,
                                evaluado_id=pasajero_id,
                                tipo='Conductor a Pasajero'
                            )
                            calificacion.puntuacion = puntuacion
                            calificacion.resena = resena
                            calificacion.save()
            else:
                # Pasajero califica al conductor
                puntuacion = int(request.POST.get('puntuacion_conductor', 0))
                resena = request.POST.get('resena_conductor', '')
                
                if 1 <= puntuacion <= 5:
                    calificacion, _ = Calificacion.objects.get_or_create(
                        viaje=viaje,
                        evaluador=request.user,
                        evaluado=viaje.conductor,
                        tipo='Pasajero a Conductor'
                    )
                    calificacion.puntuacion = puntuacion
                    calificacion.resena = resena
                    calificacion.save()
            
            messages.success(request, 'Calificación registrada correctamente')
            return redirect('trips:trip_detail', trip_id=trip_id)
        except Exception as e:
            messages.error(request, f'Error al guardar calificación: {str(e)}')
    
    # Preparar contexto
    pasajeros_confirmados = viaje.solicitudes_pasajeros.filter(estado='Confirmada').select_related('pasajero')
    
    context = {
        'viaje': viaje,
        'es_conductor': es_conductor,
        'es_pasajero': es_pasajero,
        'pasajeros_confirmados': pasajeros_confirmados,
    }
    return render(request, 'ratings/rate_users.html', context)
