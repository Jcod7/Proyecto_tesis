from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Cliente

@login_required
def cliente_list(request):
    """Lista de clientes - CU-R03, CU-R04"""
    clientes = Cliente.objects.filter(is_active=True)
    
    # Búsqueda
    search = request.GET.get('search')
    if search:
        clientes = clientes.filter(
            Q(nombre__icontains=search) |
            Q(apellido__icontains=search) |
            Q(razon_social__icontains=search) |
            Q(email__icontains=search)
        )
    
    return render(request, 'clientes/list.html', {
        'clientes': clientes,
        'search': search
    })

@login_required
def cliente_create(request):
    """Crear cliente - CU-R03, CU-R04"""
    if request.method == 'POST':
        try:
            cliente = Cliente.objects.create(
                tipo=request.POST['tipo'],
                email=request.POST['email'],
                telefono=request.POST['telefono'],
                direccion=request.POST['direccion'],
                ciudad=request.POST['ciudad'],
                nombre=request.POST.get('nombre', ''),
                apellido=request.POST.get('apellido', ''),
                razon_social=request.POST.get('razon_social', ''),
                ruc=request.POST.get('ruc', ''),
                contacto_principal=request.POST.get('contacto_principal', ''),
                observaciones=request.POST.get('observaciones', ''),
                created_by=request.user
            )
            messages.success(request, 'Cliente creado exitosamente')
            return redirect('clientes:detail', pk=cliente.pk)
        except Exception as e:
            messages.error(request, f'Error al crear cliente: {e}')
    
    return render(request, 'clientes/form.html', {'action': 'Crear'})

@login_required
def cliente_detail(request, pk):
    """Detalle de cliente"""
    cliente = get_object_or_404(Cliente, pk=pk, is_active=True)
    vehiculos = cliente.vehiculos.filter(is_active=True)
    ordenes = cliente.ordenes.filter(is_active=True)[:5]
    
    return render(request, 'clientes/detail.html', {
        'cliente': cliente,
        'vehiculos': vehiculos,
        'ordenes': ordenes
    })

