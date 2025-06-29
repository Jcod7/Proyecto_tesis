from django.db import models
from django.utils import timezone
from apps.clientes.models import Cliente
from apps.vehiculos.models import Vehiculo
from apps.accounts.models import CustomUser
import datetime

class OrdenTrabajo(models.Model):
    """Modelo para órdenes de trabajo - CU-R06"""
    
    ESTADO_CHOICES = [
        ('RECIBIDO', 'Recibido'),
        ('DIAGNOSTICO', 'En Diagnóstico'),
        ('PRESUPUESTO', 'Presupuesto Enviado'),
        ('APROBADO', 'Aprobado'),
        ('EN_TRABAJO', 'En Trabajo'),
        ('FINALIZADO', 'Finalizado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('BAJA', 'Baja'),
        ('NORMAL', 'Normal'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]
    
    numero_orden = models.CharField(max_length=20, unique=True, blank=True)
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ordenes')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='ordenes')
    
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_estimada_entrega = models.DateField(null=True, blank=True)
    fecha_entrega_real = models.DateTimeField(null=True, blank=True)
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='RECIBIDO')
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='NORMAL')
    
    kilometraje_ingreso = models.PositiveIntegerField()
    descripcion_falla = models.TextField()
    diagnostico = models.TextField(blank=True, default="")
    trabajos_realizados = models.TextField(blank=True, default="")
    
    costo_mano_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    costo_repuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    observaciones = models.TextField(blank=True, default="")
    notas_internas = models.TextField(blank=True, default="")
    
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Orden {self.numero_orden} - {self.vehiculo} - {self.get_estado_display()}"
    
    def get_dias_en_taller(self):
        if self.fecha_entrega_real:
            return (self.fecha_entrega_real.date() - self.fecha_ingreso.date()).days
        return (timezone.now().date() - self.fecha_ingreso.date()).days
    
    def is_atrasado(self):
        if self.fecha_estimada_entrega and self.estado not in ['ENTREGADO', 'CANCELADO']:
            return timezone.now().date() > self.fecha_estimada_entrega
        return False
    
    def save(self, *args, **kwargs):
        # Generar número de orden automáticamente solo si no existe
        if not self.numero_orden:
            year = datetime.datetime.now().year
            count = OrdenTrabajo.objects.filter(
                numero_orden__startswith=f"OT-{year}"
            ).count() + 1
            self.numero_orden = f"OT-{year}-{count:04d}"
        
        # Calcular costo total automáticamente
        self.costo_total = self.costo_mano_obra + self.costo_repuestos
        
        # Actualizar kilometraje si es mayor al actual del vehículo
        if self.kilometraje_ingreso > self.vehiculo.kilometraje:
            self.vehiculo.kilometraje = self.kilometraje_ingreso
            self.vehiculo.save()
        
        super().save(*args, **kwargs)
