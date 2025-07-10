from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import OrdenTrabajo
from apps.clientes.models import Cliente
from apps.vehiculos.models import Vehiculo

def orden_list(request):
    """Lista de órdenes - CU-R06"""
    ordenes = OrdenTrabajo.objects.filter(is_active=True).select_related('cliente', 'vehiculo')
    
    # Filtros
    estado = request.GET.get('estado')
    if estado:
        ordenes = ordenes.filter(estado=estado)
    
    search = request.GET.get('search')
    if search:
        ordenes = ordenes.filter(
            Q(numero_orden__icontains=search) |
            Q(cliente__nombre__icontains=search) |
            Q(vehiculo__placa__icontains=search)
        )
    
    return render(request, 'ordenes/list.html', {
        'ordenes': ordenes,
        'estados': OrdenTrabajo.ESTADO_CHOICES,
        'search': search,
        'estado_filter': estado
    })

def orden_create(request):
    """Crear orden - CU-R06"""
    clientes = Cliente.objects.filter(is_active=True)
    
    if request.method == 'POST':
        try:
            # Validar que los campos requeridos estén presentes
            kilometraje = request.POST.get('kilometraje_ingreso', '').strip()
            if not kilometraje:
                raise ValueError("El kilometraje de ingreso es requerido")
            
            orden = OrdenTrabajo.objects.create(
                cliente_id=request.POST['cliente'],
                vehiculo_id=request.POST['vehiculo'],
                kilometraje_ingreso=int(kilometraje),
                descripcion_falla=request.POST['descripcion_falla'],
                fecha_estimada_entrega=request.POST.get('fecha_estimada_entrega') or None,
                prioridad=request.POST.get('prioridad', 'NORMAL'),
                observaciones=request.POST.get('observaciones', ''),
                # created_by=request.user if request.user.is_authenticated else None
            )
            messages.success(request, f'Orden {orden.numero_orden} creada exitosamente')
            return redirect('ordenes:detail', pk=orden.pk)
        except Exception as e:
            messages.error(request, f'Error al crear orden: {e}')
    
    return render(request, 'ordenes/form.html', {
        'clientes': clientes,
        'action': 'Crear'
    })

def orden_detail(request, pk):
    """Detalle de orden"""
    orden = get_object_or_404(OrdenTrabajo, pk=pk, is_active=True)
    
    return render(request, 'ordenes/detail.html', {
        'orden': orden,
        'dias_en_taller': orden.get_dias_en_taller(),
        'is_atrasado': orden.is_atrasado()
    })

def load_vehiculos(request):
    """AJAX para cargar vehículos por cliente"""
    cliente_id = request.GET.get('cliente_id')
    vehiculos = Vehiculo.objects.filter(
        cliente_id=cliente_id,
        is_active=True
    ).values('id', 'marca', 'modelo', 'anio', 'placa', 'kilometraje')
    
    return JsonResponse(list(vehiculos), safe=False)

def orden_edit(request, pk):
    """Editar orden"""
    orden = get_object_or_404(OrdenTrabajo, pk=pk, is_active=True)
    clientes = Cliente.objects.filter(is_active=True)
    
    if request.method == 'POST':
        try:
            # Validar que los campos requeridos estén presentes
            kilometraje = request.POST.get('kilometraje_ingreso', '').strip()
            if not kilometraje:
                raise ValueError("El kilometraje de ingreso es requerido")
            
            orden.cliente_id = request.POST['cliente']
            orden.vehiculo_id = request.POST['vehiculo']
            orden.kilometraje_ingreso = int(kilometraje)
            orden.descripcion_falla = request.POST['descripcion_falla']
            orden.fecha_estimada_entrega = request.POST.get('fecha_estimada_entrega') or None
            orden.prioridad = request.POST.get('prioridad', 'NORMAL')
            orden.observaciones = request.POST.get('observaciones', '')
            orden.estado = request.POST.get('estado', orden.estado)
            orden.save()
            
            messages.success(request, f'Orden {orden.numero_orden} actualizada exitosamente')
            return redirect('ordenes:detail', pk=orden.pk)
        except Exception as e:
            messages.error(request, f'Error al actualizar orden: {e}')
    
    return render(request, 'ordenes/form.html', {
        'orden': orden,
        'clientes': clientes,
        'action': 'Editar'
    })

def orden_delete(request, pk):
    """Eliminar orden (soft delete)"""
    orden = get_object_or_404(OrdenTrabajo, pk=pk, is_active=True)
    
    if request.method == 'POST':
        orden.is_active = False
        orden.save()
        messages.success(request, f'Orden {orden.numero_orden} eliminada exitosamente')
        return redirect('ordenes:list')
    
    return render(request, 'ordenes/detail.html', {
        'orden': orden,
        'confirm_delete': True
    })