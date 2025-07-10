from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Min, Max, Count
from .models import Vehiculo
from apps.clientes.models import Cliente

def vehiculo_list(request):
    """Lista de vehículos - CU-R05"""
    vehiculos = Vehiculo.objects.filter(is_active=True).select_related('cliente')
    
    search = request.GET.get('search')
    if search:
        vehiculos = vehiculos.filter(
            Q(marca__icontains=search) |
            Q(modelo__icontains=search) |
            Q(placa__icontains=search) |
            Q(cliente__nombre__icontains=search) |
            Q(cliente__razon_social__icontains=search)
        )
    
    # Estadísticas para el dashboard
    stats = vehiculos.aggregate(
        total_vehiculos=Count('id'),
        anio_mas_antiguo=Min('anio'),
        anio_mas_reciente=Max('anio')
    )
    
    return render(request, 'vehiculos/list.htm', {
        'vehiculos': vehiculos,
        'search': search,
        'stats': stats
    })

def vehiculo_create(request):
    """Crear vehículo - CU-R05"""
    clientes = Cliente.objects.filter(is_active=True)
    
    if request.method == 'POST':
        try:
            # Validar campos numéricos
            anio = request.POST.get('anio', '').strip()
            kilometraje = request.POST.get('kilometraje', '').strip()
            
            if not anio:
                raise ValueError("El año es requerido")
            if not kilometraje:
                raise ValueError("El kilometraje es requerido")
            
            vehiculo = Vehiculo.objects.create(
                cliente_id=request.POST['cliente'],
                tipo_vehiculo=request.POST['tipo_vehiculo'],
                marca=request.POST['marca'],
                modelo=request.POST['modelo'],
                anio=int(anio),
                placa=request.POST['placa'],
                color=request.POST['color'],
                tipo_combustible=request.POST['tipo_combustible'],
                tipo_transmision=request.POST['tipo_transmision'],
                kilometraje=int(kilometraje),
                vin=request.POST.get('vin', ''),
                observaciones=request.POST.get('observaciones', ''),
                # created_by=request.user if request.user.is_authenticated else None
            )
            messages.success(request, 'Vehículo registrado exitosamente')
            return redirect('vehiculos:detail', pk=vehiculo.pk)
        except Exception as e:
            messages.error(request, f'Error al registrar vehículo: {e}')
    
    return render(request, 'vehiculos/form.html', {
        'clientes': clientes,
        'action': 'Registrar'
    })

def vehiculo_detail(request, pk):
    """Detalle de vehículo"""
    vehiculo = get_object_or_404(Vehiculo, pk=pk, is_active=True)
    ordenes = vehiculo.ordenes.filter(is_active=True)[:5]
    
    return render(request, 'vehiculos/detail.htm', {
        'vehiculo': vehiculo,
        'ordenes': ordenes
    })

def vehiculo_edit(request, pk):
    """Editar vehículo"""
    vehiculo = get_object_or_404(Vehiculo, pk=pk, is_active=True)
    clientes = Cliente.objects.filter(is_active=True)
    
    if request.method == 'POST':
        try:
            # Validar campos numéricos
            anio = request.POST.get('anio', '').strip()
            kilometraje = request.POST.get('kilometraje', '').strip()
            
            if not anio:
                raise ValueError("El año es requerido")
            if not kilometraje:
                raise ValueError("El kilometraje es requerido")
            
            vehiculo.cliente_id = request.POST['cliente']
            vehiculo.tipo_vehiculo = request.POST['tipo_vehiculo']
            vehiculo.marca = request.POST['marca']
            vehiculo.modelo = request.POST['modelo']
            vehiculo.anio = int(anio)
            vehiculo.placa = request.POST['placa']
            vehiculo.color = request.POST['color']
            vehiculo.tipo_combustible = request.POST['tipo_combustible']
            vehiculo.tipo_transmision = request.POST['tipo_transmision']
            vehiculo.kilometraje = int(kilometraje)
            vehiculo.vin = request.POST.get('vin', '')
            vehiculo.observaciones = request.POST.get('observaciones', '')
            vehiculo.save()
            
            messages.success(request, 'Vehículo actualizado exitosamente')
            return redirect('vehiculos:detail', pk=vehiculo.pk)
        except Exception as e:
            messages.error(request, f'Error al actualizar vehículo: {e}')
    
    return render(request, 'vehiculos/form.html', {
        'vehiculo': vehiculo,
        'clientes': clientes,
        'action': 'Editar'
    })

def vehiculo_delete(request, pk):
    """Eliminar vehículo (soft delete)"""
    vehiculo = get_object_or_404(Vehiculo, pk=pk, is_active=True)
    
    if request.method == 'POST':
        vehiculo.is_active = False
        vehiculo.save()
        messages.success(request, 'Vehículo eliminado exitosamente')
        return redirect('vehiculos:list')
    
    return render(request, 'vehiculos/detail.htm', {
        'vehiculo': vehiculo,
        'confirm_delete': True
    })