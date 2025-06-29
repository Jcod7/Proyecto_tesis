from django.db import models
from apps.clientes.models import Cliente
from apps.accounts.models import CustomUser

class EspacioTaller(models.Model):
    """Espacios físicos del taller"""
    
    TIPO_CHOICES = [
        ('ELEVADOR', 'Elevador'),
        ('FOSA', 'Fosa'),
        ('PATIO', 'Patio'),
    ]
    
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class Vehiculo(models.Model):
    """Modelo para vehículos - CU-R05"""
    
    TIPO_CHOICES = [
        ('AUTO', 'Automóvil'),
        ('CAMIONETA', 'Camioneta'),
        ('CAMION', 'Camión'),
        ('MOTO', 'Motocicleta'),
    ]
    
    COMBUSTIBLE_CHOICES = [
        ('GASOLINA', 'Gasolina'),
        ('DIESEL', 'Diésel'),
        ('GAS', 'Gas'),
    ]
    
    TRANSMISION_CHOICES = [
        ('MANUAL', 'Manual'),
        ('AUTOMATICA', 'Automática'),
    ]
    
    # Relación con cliente
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos')
    
    # Información básica
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='AUTO')
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    placa = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=30)
    
    # Especificaciones técnicas
    tipo_combustible = models.CharField(max_length=20, choices=COMBUSTIBLE_CHOICES, default='GASOLINA')
    tipo_transmision = models.CharField(max_length=20, choices=TRANSMISION_CHOICES, default='MANUAL')
    kilometraje = models.PositiveIntegerField(default=0)
    
    # Información adicional
    vin = models.CharField(max_length=17, blank=True)
    observaciones = models.TextField(blank=True, default="")
    
    # Espacio asignado
    espacio_asignado = models.ForeignKey(EspacioTaller, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Control
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.marca} {self.modelo} {self.anio} - {self.placa}"
    
    def get_identificacion(self):
        return f"{self.marca} {self.modelo} {self.anio} - Placa: {self.placa}"
    
    def save(self, *args, **kwargs):
        # Convertir placa a mayúsculas
        if self.placa:
            self.placa = self.placa.upper()
        
        # Asignar espacio automáticamente si no tiene
        if not self.espacio_asignado:
            espacio_disponible = EspacioTaller.objects.filter(disponible=True).first()
            if espacio_disponible:
                self.espacio_asignado = espacio_disponible
                espacio_disponible.disponible = False
                espacio_disponible.save()
        
        super().save(*args, **kwargs)