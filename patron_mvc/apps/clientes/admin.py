from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_completo', 'tipo', 'email', 'telefono', 'ciudad', 'created_at')  # ← Cambiar aquí
    list_filter = ('tipo', 'ciudad', 'created_at')  # ← Cambiar aquí
    search_fields = ('nombre', 'apellido', 'razon_social', 'email', 'telefono', 'ruc')
    
    def get_nombre_completo(self, obj):
        return obj.get_nombre_completo()
    get_nombre_completo.short_description = 'Nombre/Razón Social'