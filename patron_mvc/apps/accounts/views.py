from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from .models import CustomUser

def user_login(request):
    """Vista de login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Verificar si el usuario está activo
            if user.activo:
                login(request, user)
                messages.success(request, f'Bienvenido {user.get_nombre_completo()}')
                return redirect('accounts:list')
            else:
                messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    """Vista de logout"""
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('accounts:login')

@login_required
def usuario_list(request):
    """Lista de usuarios"""
    usuarios = CustomUser.objects.all().order_by('-created_at')
    
    # Búsqueda
    search = request.GET.get('search')
    if search:
        usuarios = usuarios.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(role__icontains=search)
        )
    
    # Filtro por rol
    role_filter = request.GET.get('role')
    if role_filter:
        usuarios = usuarios.filter(role=role_filter)
    
    # Filtro por estado
    status_filter = request.GET.get('status')
    if status_filter:
        usuarios = usuarios.filter(activo=status_filter == 'true')
    
    return render(request, 'accounts/list.html', {
        'usuarios': usuarios,
        'search': search,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'roles': CustomUser.ROLE_CHOICES
    })

@login_required
def usuario_create(request):
    """Crear usuario"""
    if request.method == 'POST':
        try:
            # Validar que las contraseñas coincidan
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 != password2:
                raise ValueError("Las contraseñas no coinciden")
            
            if len(password1) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")
            
            usuario = CustomUser.objects.create(
                username=request.POST['username'],
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
                email=request.POST.get('email', ''),
                role=request.POST.get('role', 'MECANICO'),
                telefono=request.POST.get('telefono', ''),
                password=make_password(password1),
                is_active=True,
                activo=True
            )
            
            messages.success(request, f'Usuario {usuario.username} creado exitosamente')
            return redirect('accounts:detail', pk=usuario.pk)
            
        except Exception as e:
            messages.error(request, f'Error al crear usuario: {e}')
    
    return render(request, 'accounts/form.html', {
        'action': 'Crear',
        'roles': CustomUser.ROLE_CHOICES
    })

@login_required
def usuario_detail(request, pk):
    """Detalle de usuario"""
    usuario = get_object_or_404(CustomUser, pk=pk)
    
    # Estadísticas del usuario
    vehiculos_registrados = 0
    ordenes_creadas = 0
    ordenes_asignadas = 0
    
    try:
        from apps.vehiculos.models import Vehiculo
        from apps.ordenes.models import OrdenTrabajo
        
        vehiculos_registrados = Vehiculo.objects.filter(created_by=usuario, is_active=True).count()
        ordenes_creadas = OrdenTrabajo.objects.filter(created_by=usuario, is_active=True).count()
        ordenes_asignadas = OrdenTrabajo.objects.filter(mecanico_asignado=usuario, is_active=True).count()
    except:
        pass
    
    return render(request, 'accounts/detail.html', {
        'usuario': usuario,
        'vehiculos_registrados': vehiculos_registrados,
        'ordenes_creadas': ordenes_creadas,
        'ordenes_asignadas': ordenes_asignadas
    })

@login_required
def usuario_edit(request, pk):
    """Editar usuario"""
    usuario = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        try:
            usuario.username = request.POST['username']
            usuario.first_name = request.POST.get('first_name', '')
            usuario.last_name = request.POST.get('last_name', '')
            usuario.email = request.POST.get('email', '')
            usuario.role = request.POST.get('role', 'MECANICO')
            usuario.telefono = request.POST.get('telefono', '')
            
            # Cambiar contraseña solo si se proporciona
            password1 = request.POST.get('password1', '').strip()
            password2 = request.POST.get('password2', '').strip()
            
            if password1:
                if password1 != password2:
                    raise ValueError("Las contraseñas no coinciden")
                if len(password1) < 6:
                    raise ValueError("La contraseña debe tener al menos 6 caracteres")
                usuario.password = make_password(password1)
            
            usuario.save()
            
            messages.success(request, f'Usuario {usuario.username} actualizado exitosamente')
            return redirect('accounts:detail', pk=usuario.pk)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar usuario: {e}')
    
    return render(request, 'accounts/form.html', {
        'usuario': usuario,
        'action': 'Editar',
        'roles': CustomUser.ROLE_CHOICES
    })

@login_required
def usuario_delete(request, pk):
    """Eliminar usuario (soft delete)"""
    usuario = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        # Verificar que no se elimine a sí mismo
        if usuario == request.user:
            messages.error(request, 'No puedes eliminar tu propio usuario')
            return redirect('accounts:detail', pk=usuario.pk)
        
        usuario.activo = False
        usuario.is_active = False
        usuario.save()
        
        messages.success(request, f'Usuario {usuario.username} eliminado exitosamente')
        return redirect('accounts:list')
    
    return render(request, 'accounts/detail.html', {
        'usuario': usuario,
        'confirm_delete': True
    })

@login_required
def usuario_toggle_status(request, pk):
    """Activar/desactivar usuario"""
    usuario = get_object_or_404(CustomUser, pk=pk)
    
    # Verificar que no se desactive a sí mismo
    if usuario == request.user:
        messages.error(request, 'No puedes desactivar tu propio usuario')
        return redirect('accounts:list')
    
    # Cambiar estado
    usuario.activo = not usuario.activo
    usuario.is_active = usuario.activo
    usuario.save()
    
    status = 'activado' if usuario.activo else 'desactivado'
    messages.success(request, f'Usuario {usuario.username} {status} exitosamente')
    
    return redirect('accounts:list')
