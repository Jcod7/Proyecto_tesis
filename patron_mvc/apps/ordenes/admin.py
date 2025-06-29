from django.contrib import admin
from .models import OrdenTrabajo

@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('numero_orden', 'get_cliente_nombre', 'get_vehiculo_info', 'estado', 'prioridad', 'fecha_ingreso', 'fecha_estimada_entrega')
    list_filter = ('estado', 'prioridad', 'fecha_ingreso', 'created_at')
    search_fields = ('numero_orden', 'cliente__nombre', 'cliente__apellido', 'cliente__razon_social', 'vehiculo__placa', 'descripcion_falla')
    readonly_fields = ('numero_orden', 'created_at', 'updated_at')
    
    def get_cliente_nombre(self, obj):
        return obj.cliente.get_nombre_completo()
    get_cliente_nombre.short_description = 'Cliente'
    
    def get_vehiculo_info(self, obj):
        return f"{obj.vehiculo.marca} {obj.vehiculo.modelo} - {obj.vehiculo.placa}"
    get_vehiculo_info.short_description = 'Vehículo'