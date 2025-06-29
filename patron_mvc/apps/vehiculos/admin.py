from django.contrib import admin
from .models import Vehiculo

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'anio', 'get_cliente_nombre', 'tipo_combustible', 'created_at')  # ← Cambiar aquí
    list_filter = ('tipo_vehiculo', 'marca', 'tipo_combustible', 'tipo_transmision', 'created_at')  # ← Cambiar aquí
    search_fields = ('placa', 'marca', 'modelo', 'vin', 'cliente__nombre', 'cliente__apellido', 'cliente__razon_social')
    
    def get_cliente_nombre(self, obj):
        return obj.cliente.get_nombre_completo()
    get_cliente_nombre.short_description = 'Cliente'