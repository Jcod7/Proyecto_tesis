#!/usr/bin/env python
"""
Script para mostrar ejemplos de los datos creados
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patron_mvc.settings')
django.setup()

from apps.accounts.models import CustomUser
from apps.clientes.models import Cliente
from apps.vehiculos.models import Vehiculo
from apps.ordenes.models import OrdenTrabajo

def mostrar_estadisticas():
    """Mostrar estadísticas de los datos"""
    print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("=" * 50)
    
    # Usuarios
    print(f"👥 USUARIOS ({CustomUser.objects.count()})")
    for role, role_name in CustomUser.ROLE_CHOICES:
        count = CustomUser.objects.filter(role=role).count()
        print(f"   - {role_name}: {count}")
    
    # Clientes
    print(f"\n👤 CLIENTES ({Cliente.objects.count()})")
    particulares = Cliente.objects.filter(tipo='PARTICULAR').count()
    empresariales = Cliente.objects.filter(tipo='EMPRESARIAL').count()
    print(f"   - Particulares: {particulares}")
    print(f"   - Empresariales: {empresariales}")
    
    # Vehículos por tipo
    print(f"\n🚗 VEHÍCULOS ({Vehiculo.objects.count()})")
    for tipo, tipo_name in Vehiculo.TIPO_CHOICES:
        count = Vehiculo.objects.filter(tipo_vehiculo=tipo).count()
        print(f"   - {tipo_name}: {count}")
    
    # Órdenes por estado
    print(f"\n📋 ÓRDENES DE TRABAJO ({OrdenTrabajo.objects.count()})")
    for estado, estado_name in OrdenTrabajo.ESTADO_CHOICES:
        count = OrdenTrabajo.objects.filter(estado=estado).count()
        print(f"   - {estado_name}: {count}")

def mostrar_ejemplos():
    """Mostrar ejemplos de datos"""
    print("\n🔍 EJEMPLOS DE DATOS CREADOS")
    print("=" * 50)
    
    # Usuarios de ejemplo
    print("👥 USUARIOS DE EJEMPLO:")
    usuarios = CustomUser.objects.all()[:5]
    for usuario in usuarios:
        print(f"   • {usuario.username} - {usuario.get_nombre_completo()} ({usuario.get_role_display()})")
    
    # Clientes de ejemplo
    print("\n👤 CLIENTES DE EJEMPLO:")
    clientes = Cliente.objects.all()[:5]
    for cliente in clientes:
        tipo_icon = "👤" if cliente.tipo == 'PARTICULAR' else "🏢"
        print(f"   {tipo_icon} {cliente.get_nombre_completo()} - {cliente.ciudad}")
    
    # Vehículos de ejemplo
    print("\n🚗 VEHÍCULOS DE EJEMPLO:")
    vehiculos = Vehiculo.objects.all()[:5]
    for vehiculo in vehiculos:
        print(f"   • {vehiculo.marca} {vehiculo.modelo} {vehiculo.anio} - {vehiculo.placa} ({vehiculo.cliente.get_nombre_completo()})")
    
    # Órdenes de ejemplo
    print("\n📋 ÓRDENES DE EJEMPLO:")
    ordenes = OrdenTrabajo.objects.all()[:5]
    for orden in ordenes:
        print(f"   • {orden.numero_orden} - {orden.vehiculo.placa} - {orden.get_estado_display()} - ${orden.costo_total:,.0f}")

def mostrar_credenciales():
    """Mostrar credenciales de acceso"""
    print("\n🔑 CREDENCIALES DE ACCESO")
    print("=" * 50)
    
    print("Para acceder al sistema usa cualquiera de estas credenciales:")
    print()
    print("👑 ADMINISTRADOR:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
    print()
    print("👨‍🔧 MECÁNICOS:")
    mecanicos = CustomUser.objects.filter(role='MECANICO')[:3]
    for mecanico in mecanicos:
        print(f"   Usuario: {mecanico.username}")
        print(f"   Contraseña: mecanico123")
    print()
    print("👩‍💼 RECEPCIONISTAS:")
    recepcionistas = CustomUser.objects.filter(role='RECEPCIONISTA')[:2]
    for recepcionista in recepcionistas:
        print(f"   Usuario: {recepcionista.username}")
        print(f"   Contraseña: recep123")
    print()
    print("👨‍💼 GERENTE:")
    print("   Usuario: gerente")
    print("   Contraseña: gerente123")

def main():
    """Función principal"""
    mostrar_estadisticas()
    mostrar_ejemplos()
    mostrar_credenciales()
    
    print("\n🌐 ACCESO AL SISTEMA")
    print("=" * 50)
    print("URL: http://0.0.0.0:8002/")
    print("URL de Admin: http://0.0.0.0:8002/admin/")
    print()
    print("✅ ¡El sistema está listo para usar!")

if __name__ == "__main__":
    main()
