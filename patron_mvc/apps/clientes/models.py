from django.db import models
from apps.accounts.models import CustomUser
from django.utils import timezone

class Cliente(models.Model):
    """Modelo base para clientes - CU-R03 y CU-R04"""
    
    TIPO_CHOICES = [
        ('PARTICULAR', 'Particular'),
        ('EMPRESARIAL', 'Empresarial'),
    ]
    
    # Campos comunes
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True, default="")
    
    # Campos para particulares (CU-R03)
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100, blank=True)
    
    # Campos para empresariales (CU-R04)
    razon_social = models.CharField(max_length=200, blank=True)
    ruc = models.CharField(max_length=13, blank=True)
    contacto_principal = models.CharField(max_length=200, blank=True)
    
    # Control
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.tipo == 'PARTICULAR':
            return f"{self.nombre} {self.apellido}"
        return self.razon_social
    
    def get_nombre_completo(self):
        """Método para obtener nombre según tipo"""
        if self.tipo == 'PARTICULAR':
            return f"{self.nombre} {self.apellido}".strip()
        return self.razon_social
    
    def save(self, *args, **kwargs):
        # Validaciones automáticas según tipo
        if self.tipo == 'PARTICULAR' and not self.nombre:
            raise ValueError("Nombre es requerido para clientes particulares")
        elif self.tipo == 'EMPRESARIAL' and not self.razon_social:
            raise ValueError("Razón social es requerida para clientes empresariales")
        
        super().save(*args, **kwargs)