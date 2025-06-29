
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('clientes:list')),  # Redirigir raíz a clientes
    path('clientes/', include('apps.clientes.urls')),      # Corregido: apps.clientes
    path('vehiculos/', include('apps.vehiculos.urls')),    # Corregido: apps.vehiculos  
    path('ordenes/', include('apps.ordenes.urls')),        # Corregido: apps.ordenes
]
