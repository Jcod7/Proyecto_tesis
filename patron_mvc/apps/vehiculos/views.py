from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Vehiculo
from apps.clientes.models import Cliente


@login_required
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
    
    return render(request, 'vehiculos/list.html', {
        'vehiculos': vehiculos,
        'search': search
    })

@login_required
def vehiculo_create(request):
    """Crear vehículo - CU-R05"""
    clientes = Cliente.objects.filter(is_active=True)
    
    if request.method == 'POST':
        try:
            vehiculo = Vehiculo.objects.create(
                cliente_id=request.POST['cliente'],
                tipo_vehiculo=request.POST['tipo_vehiculo'],
                marca=request.POST['marca'],
                modelo=request.POST['modelo'],
                anio=request.POST['anio'],
                placa=request.POST['placa'],
                color=request.POST['color'],
                tipo_combustible=request.POST['tipo_combustible'],
                tipo_transmision=request.POST['tipo_transmision'],
                kilometraje=request.POST['kilometraje'],
                vin=request.POST.get('vin', ''),
                observaciones=request.POST.get('observaciones', ''),
                created_by=request.user
            )
            messages.success(request, 'Vehículo registrado exitosamente')
            return redirect('vehiculos:detail', pk=vehiculo.pk)
        except Exception as e:
            messages.error(request, f'Error al registrar vehículo: {e}')
    
    return render(request, 'vehiculos/form.html', {
        'clientes': clientes,
        'action': 'Registrar'
    })

@login_required
def vehiculo_detail(request, pk):
    """Detalle de vehículo"""
    vehiculo = get_object_or_404(Vehiculo, pk=pk, is_active=True)
    ordenes = vehiculo.ordenes.filter(is_active=True)[:5]
    
    return render(request, 'vehiculos/detail.html', {
        'vehiculo': vehiculo,
        'ordenes': ordenes
    })