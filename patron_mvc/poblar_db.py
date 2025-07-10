#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de prueba realistas
"""
import os
import sys
import django
from django.utils import timezone
from datetime import datetime, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patron_mvc.settings')
django.setup()

from apps.accounts.models import CustomUser
from apps.clientes.models import Cliente
from apps.vehiculos.models import Vehiculo
from apps.ordenes.models import OrdenTrabajo

def crear_usuarios():
    """Crear usuarios del sistema"""
    print("Creando usuarios...")
    
    # Admin
    admin, created = CustomUser.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'email': 'admin@taller.com',
            'role': 'ADMIN',
            'telefono': '555-0001',
            'is_superuser': True,
            'is_staff': True,
            'activo': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
    
    # Mecánicos
    mecanicos_data = [
        ('carlos_rodriguez', 'Carlos', 'Rodríguez', 'carlos@taller.com', '555-1001'),
        ('maria_gonzalez', 'María', 'González', 'maria@taller.com', '555-1002'),
        ('jose_martinez', 'José', 'Martínez', 'jose@taller.com', '555-1003'),
        ('ana_lopez', 'Ana', 'López', 'ana@taller.com', '555-1004'),
        ('luis_fernandez', 'Luis', 'Fernández', 'luis@taller.com', '555-1005'),
    ]
    
    for username, nombre, apellido, email, telefono in mecanicos_data:
        mecanico, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                'first_name': nombre,
                'last_name': apellido,
                'email': email,
                'role': 'MECANICO',
                'telefono': telefono,
                'activo': True
            }
        )
        if created:
            mecanico.set_password('mecanico123')
            mecanico.save()
    
    # Recepcionistas
    recepcionistas_data = [
        ('patricia_silva', 'Patricia', 'Silva', 'patricia@taller.com', '555-2001'),
        ('carmen_ruiz', 'Carmen', 'Ruiz', 'carmen@taller.com', '555-2002'),
    ]
    
    for username, nombre, apellido, email, telefono in recepcionistas_data:
        recepcionista, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                'first_name': nombre,
                'last_name': apellido,
                'email': email,
                'role': 'RECEPCIONISTA',
                'telefono': telefono,
                'activo': True
            }
        )
        if created:
            recepcionista.set_password('recep123')
            recepcionista.save()
    
    # Gerente
    gerente, created = CustomUser.objects.get_or_create(
        username='gerente',
        defaults={
            'first_name': 'Roberto',
            'last_name': 'Manager',
            'email': 'gerente@taller.com',
            'role': 'GERENTE',
            'telefono': '555-3001',
            'activo': True
        }
    )
    if created:
        gerente.set_password('gerente123')
        gerente.save()
    
    print(f"✓ Usuarios creados: {CustomUser.objects.count()}")

def crear_clientes():
    """Crear clientes particulares y empresariales"""
    print("Creando clientes...")
    
    # Clientes particulares
    clientes_particulares = [
        ('Juan', 'Pérez', 'juan.perez@email.com', '555-4001', 'Calle 123 #45-67', 'Bogotá'),
        ('María', 'García', 'maria.garcia@email.com', '555-4002', 'Carrera 89 #12-34', 'Medellín'),
        ('Carlos', 'López', 'carlos.lopez@email.com', '555-4003', 'Avenida 56 #78-90', 'Cali'),
        ('Ana', 'Martínez', 'ana.martinez@email.com', '555-4004', 'Calle 34 #12-56', 'Barranquilla'),
        ('Luis', 'Rodríguez', 'luis.rodriguez@email.com', '555-4005', 'Carrera 23 #67-89', 'Bucaramanga'),
        ('Carmen', 'Fernández', 'carmen.fernandez@email.com', '555-4006', 'Avenida 45 #23-45', 'Cartagena'),
        ('Roberto', 'Sánchez', 'roberto.sanchez@email.com', '555-4007', 'Calle 67 #89-01', 'Pereira'),
        ('Patricia', 'Gómez', 'patricia.gomez@email.com', '555-4008', 'Carrera 12 #34-56', 'Manizales'),
        ('Miguel', 'Torres', 'miguel.torres@email.com', '555-4009', 'Avenida 78 #90-12', 'Ibagué'),
        ('Elena', 'Vargas', 'elena.vargas@email.com', '555-4010', 'Calle 90 #12-34', 'Santa Marta'),
        ('Diego', 'Castillo', 'diego.castillo@email.com', '555-4011', 'Carrera 56 #78-90', 'Villavicencio'),
        ('Sofía', 'Herrera', 'sofia.herrera@email.com', '555-4012', 'Avenida 23 #45-67', 'Neiva'),
        ('Andrés', 'Jiménez', 'andres.jimenez@email.com', '555-4013', 'Calle 45 #67-89', 'Popayán'),
        ('Lucía', 'Morales', 'lucia.morales@email.com', '555-4014', 'Carrera 67 #89-01', 'Pasto'),
        ('Javier', 'Ortiz', 'javier.ortiz@email.com', '555-4015', 'Avenida 89 #01-23', 'Tunja'),
        ('Valentina', 'Ramírez', 'valentina.ramirez@email.com', '555-4016', 'Calle 12 #34-56', 'Armenia'),
        ('Sebastián', 'Cruz', 'sebastian.cruz@email.com', '555-4017', 'Carrera 34 #56-78', 'Montería'),
        ('Isabella', 'Mendoza', 'isabella.mendoza@email.com', '555-4018', 'Avenida 56 #78-90', 'Sincelejo'),
        ('Mateo', 'Restrepo', 'mateo.restrepo@email.com', '555-4019', 'Calle 78 #90-12', 'Riohacha'),
        ('Camila', 'Ospina', 'camila.ospina@email.com', '555-4020', 'Carrera 90 #12-34', 'Valledupar'),
        ('Santiago', 'Delgado', 'santiago.delgado@email.com', '555-4021', 'Avenida 12 #34-56', 'Florencia'),
        ('Martina', 'Vásquez', 'martina.vasquez@email.com', '555-4022', 'Calle 34 #56-78', 'Quibdó'),
        ('Nicolás', 'Aguilar', 'nicolas.aguilar@email.com', '555-4023', 'Carrera 56 #78-90', 'Mocoa'),
        ('Salomé', 'Pineda', 'salome.pineda@email.com', '555-4024', 'Avenida 78 #90-12', 'Yopal'),
        ('Emilio', 'Navarro', 'emilio.navarro@email.com', '555-4025', 'Calle 90 #12-34', 'Leticia'),
        ('Daniela', 'Rojas', 'daniela.rojas@email.com', '555-4026', 'Carrera 12 #34-56', 'Inírida'),
        ('Gabriel', 'Campos', 'gabriel.campos@email.com', '555-4027', 'Avenida 34 #56-78', 'San José'),
        ('Mariana', 'Parra', 'mariana.parra@email.com', '555-4028', 'Calle 56 #78-90', 'Mitú'),
        ('Alejandro', 'Ramos', 'alejandro.ramos@email.com', '555-4029', 'Carrera 78 #90-12', 'Puerto Carreño'),
        ('Valeria', 'Guerrero', 'valeria.guerrero@email.com', '555-4030', 'Avenida 90 #12-34', 'Arauca'),
    ]
    
    created_by = CustomUser.objects.filter(role='RECEPCIONISTA').first()
    
    for nombre, apellido, email, telefono, direccion, ciudad in clientes_particulares:
        Cliente.objects.get_or_create(
            email=email,
            defaults={
                'tipo': 'PARTICULAR',
                'nombre': nombre,
                'apellido': apellido,
                'telefono': telefono,
                'direccion': direccion,
                'ciudad': ciudad,
                'created_by': created_by,
                'is_active': True
            }
        )
    
    # Clientes empresariales
    clientes_empresariales = [
        ('Transportes Rápidos S.A.S.', '901234567-1', 'Juan Carlos Pérez', 'contacto@transportesrapidos.com', '555-5001', 'Zona Industrial Norte', 'Bogotá'),
        ('Logística Express Ltda.', '901234568-2', 'María Fernanda García', 'info@logisticaexpress.com', '555-5002', 'Carrera 45 #67-89', 'Medellín'),
        ('Flota Andina S.A.', '901234569-3', 'Carlos Eduardo López', 'gerencia@flotaandina.com', '555-5003', 'Avenida 30 #45-67', 'Cali'),
        ('Servicios de Carga Ltda.', '901234570-4', 'Ana Lucía Martínez', 'servicios@cargaltda.com', '555-5004', 'Calle 123 #45-67', 'Barranquilla'),
        ('Transporte Comercial S.A.S.', '901234571-5', 'Luis Alberto Rodríguez', 'comercial@transcomercial.com', '555-5005', 'Carrera 67 #89-01', 'Bucaramanga'),
        ('Distribuidora del Caribe', '901234572-6', 'Carmen Rosa Fernández', 'distribucion@caribe.com', '555-5006', 'Avenida 89 #12-34', 'Cartagena'),
        ('Empresa de Taxis Unidos', '901234573-7', 'Roberto Sánchez', 'taxis@unidos.com', '555-5007', 'Calle 56 #78-90', 'Pereira'),
        ('Cooperativa de Transporte', '901234574-8', 'Patricia Gómez', 'cooperativa@transporte.com', '555-5008', 'Carrera 23 #45-67', 'Manizales'),
        ('Vehículos Empresariales S.A.', '901234575-9', 'Miguel Torres', 'vehiculos@empresariales.com', '555-5009', 'Avenida 12 #34-56', 'Ibagué'),
        ('Transporte Turístico Ltda.', '901234576-0', 'Elena Vargas', 'turismo@transporte.com', '555-5010', 'Calle 34 #56-78', 'Santa Marta'),
        ('Servicios Ejecutivos S.A.S.', '901234577-1', 'Diego Castillo', 'ejecutivos@servicios.com', '555-5011', 'Carrera 78 #90-12', 'Villavicencio'),
        ('Flota Urbana', '901234578-2', 'Sofía Herrera', 'urbana@flota.com', '555-5012', 'Avenida 56 #78-90', 'Neiva'),
        ('Transporte Especializado', '901234579-3', 'Andrés Jiménez', 'especializado@transporte.com', '555-5013', 'Calle 90 #12-34', 'Popayán'),
        ('Distribuciones del Sur', '901234580-4', 'Lucía Morales', 'distribuciones@sur.com', '555-5014', 'Carrera 12 #34-56', 'Pasto'),
        ('Transporte Intermunicipal', '901234581-5', 'Javier Ortiz', 'intermunicipal@transporte.com', '555-5015', 'Avenida 34 #56-78', 'Tunja'),
        ('Servicios Logísticos S.A.', '901234582-6', 'Valentina Ramírez', 'logisticos@servicios.com', '555-5016', 'Calle 67 #89-01', 'Armenia'),
        ('Empresa de Mudanzas', '901234583-7', 'Sebastián Cruz', 'mudanzas@empresa.com', '555-5017', 'Carrera 89 #01-23', 'Montería'),
        ('Transporte de Carga Pesada', '901234584-8', 'Isabella Mendoza', 'carga@pesada.com', '555-5018', 'Avenida 23 #45-67', 'Sincelejo'),
        ('Vehículos de Alquiler', '901234585-9', 'Mateo Restrepo', 'alquiler@vehiculos.com', '555-5019', 'Calle 45 #67-89', 'Riohacha'),
        ('Servicios de Transporte', '901234586-0', 'Camila Ospina', 'servicios@transporte.com', '555-5020', 'Carrera 56 #78-90', 'Valledupar'),
    ]
    
    for razon_social, ruc, contacto, email, telefono, direccion, ciudad in clientes_empresariales:
        Cliente.objects.get_or_create(
            email=email,
            defaults={
                'tipo': 'EMPRESARIAL',
                'razon_social': razon_social,
                'ruc': ruc,
                'contacto_principal': contacto,
                'telefono': telefono,
                'direccion': direccion,
                'ciudad': ciudad,
                'created_by': created_by,
                'is_active': True
            }
        )
    
    print(f"✓ Clientes creados: {Cliente.objects.count()}")

def crear_vehiculos():
    """Crear vehículos para los clientes"""
    print("Creando vehículos...")
    
    # Datos de vehículos realistas
    marcas_modelos = [
        ('Toyota', ['Corolla', 'Camry', 'Hilux', 'Prado', 'Yaris', 'Rav4']),
        ('Chevrolet', ['Spark', 'Cruze', 'Captiva', 'Aveo', 'Tracker', 'Tahoe']),
        ('Renault', ['Logan', 'Sandero', 'Duster', 'Megane', 'Fluence', 'Koleos']),
        ('Nissan', ['Sentra', 'Versa', 'Qashqai', 'X-Trail', 'Frontier', 'Pathfinder']),
        ('Hyundai', ['Accent', 'Elantra', 'Tucson', 'Santa Fe', 'i10', 'i20']),
        ('Kia', ['Picanto', 'Rio', 'Cerato', 'Sportage', 'Sorento', 'Soul']),
        ('Mazda', ['2', '3', 'CX-5', 'CX-3', '6', 'CX-9']),
        ('Ford', ['Fiesta', 'Focus', 'EcoSport', 'Escape', 'Explorer', 'F-150']),
        ('Volkswagen', ['Gol', 'Polo', 'Jetta', 'Tiguan', 'Passat', 'Amarok']),
        ('Honda', ['City', 'Civic', 'Accord', 'CR-V', 'HR-V', 'Pilot']),
    ]
    
    colores = ['Blanco', 'Negro', 'Gris', 'Rojo', 'Azul', 'Plata', 'Dorado', 'Verde', 'Amarillo', 'Beige']
    tipos_vehiculo = ['AUTO', 'CAMIONETA', 'CAMION', 'MOTO']
    combustibles = ['GASOLINA', 'DIESEL', 'GAS']
    transmisiones = ['MANUAL', 'AUTOMATICA']
    
    clientes = list(Cliente.objects.all())
    created_by = CustomUser.objects.filter(role='RECEPCIONISTA').first()
    
    # Crear vehículos para cada cliente
    for cliente in clientes:
        # Cada cliente puede tener 1-3 vehículos
        num_vehiculos = random.randint(1, 3)
        
        for i in range(num_vehiculos):
            marca, modelos = random.choice(marcas_modelos)
            modelo = random.choice(modelos)
            anio = random.randint(2015, 2024)
            color = random.choice(colores)
            tipo_vehiculo = random.choice(tipos_vehiculo)
            combustible = random.choice(combustibles)
            transmision = random.choice(transmisiones)
            kilometraje = random.randint(5000, 150000)
            
            # Generar placa única
            placa = f"{random.choice(['ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQR', 'STU', 'VWX', 'YZ1'])}-{random.randint(100, 999)}"
            
            # Verificar que la placa no exista
            while Vehiculo.objects.filter(placa=placa).exists():
                placa = f"{random.choice(['ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQR', 'STU', 'VWX', 'YZ1'])}-{random.randint(100, 999)}"
            
            # Generar VIN opcional
            vin = f"WBA{random.randint(100000, 999999)}{random.randint(10000, 99999)}" if random.random() > 0.5 else ""
            
            Vehiculo.objects.create(
                cliente=cliente,
                tipo_vehiculo=tipo_vehiculo,
                marca=marca,
                modelo=modelo,
                anio=anio,
                placa=placa,
                color=color,
                tipo_combustible=combustible,
                tipo_transmision=transmision,
                kilometraje=kilometraje,
                vin=vin,
                observaciones=f"Vehículo {marca} {modelo} {anio} del cliente {cliente.get_nombre_completo()}",
                created_by=created_by,
                is_active=True
            )
    
    print(f"✓ Vehículos creados: {Vehiculo.objects.count()}")

def crear_ordenes():
    """Crear órdenes de trabajo"""
    print("Creando órdenes de trabajo...")
    
    # Descripciones de fallas comunes
    fallas_comunes = [
        "Ruido extraño en el motor al acelerar",
        "Vibración en el volante a alta velocidad",
        "Frenos hacen ruido al frenar",
        "Aire acondicionado no enfría",
        "Cambio de aceite y filtros",
        "Revisión de suspensión",
        "Problema con la batería",
        "Luces no funcionan correctamente",
        "Problema con el sistema de escape",
        "Revisión general del vehículo",
        "Cambio de llantas",
        "Alineación y balanceo",
        "Problema con el embrague",
        "Fuga de aceite",
        "Sobrecalentamiento del motor",
        "Problema con el alternador",
        "Cambio de pastillas de freno",
        "Revisión del sistema eléctrico",
        "Problema con la dirección",
        "Mantenimiento preventivo",
    ]
    
    # Trabajos realizados
    trabajos_realizados = [
        "Cambio de aceite y filtros",
        "Revisión completa del motor",
        "Reparación del sistema de frenos",
        "Mantenimiento del aire acondicionado",
        "Alineación y balanceo",
        "Cambio de pastillas de freno",
        "Reparación del sistema eléctrico",
        "Cambio de batería",
        "Revisión de suspensión",
        "Reparación del sistema de escape",
        "Cambio de llantas",
        "Mantenimiento preventivo",
        "Reparación del embrague",
        "Reparación de fugas",
        "Revisión del sistema de enfriamiento",
        "Cambio de alternador",
        "Reparación de luces",
        "Ajuste de dirección",
        "Sincronización del motor",
        "Limpieza de inyectores",
    ]
    
    estados = ['RECIBIDO', 'DIAGNOSTICO', 'PRESUPUESTO', 'APROBADO', 'EN_TRABAJO', 'FINALIZADO', 'ENTREGADO', 'CANCELADO']
    prioridades = ['BAJA', 'NORMAL', 'ALTA', 'URGENTE']
    
    vehiculos = list(Vehiculo.objects.all())
    mecanicos = list(CustomUser.objects.filter(role='MECANICO'))
    created_by = CustomUser.objects.filter(role='RECEPCIONISTA').first()
    
    # Crear órdenes
    for i in range(75):  # 75 órdenes para tener variedad
        vehiculo = random.choice(vehiculos)
        mecanico = random.choice(mecanicos)
        
        # Fecha de ingreso entre 1 y 30 días atrás
        fecha_ingreso = timezone.now() - timedelta(days=random.randint(1, 30))
        
        # Fecha estimada de entrega
        fecha_estimada = fecha_ingreso + timedelta(days=random.randint(1, 7))
        
        # Estado y fechas coherentes
        estado = random.choice(estados)
        fecha_entrega_real = None
        
        if estado == 'ENTREGADO':
            fecha_entrega_real = fecha_estimada + timedelta(days=random.randint(-2, 3))
        
        # Costos realistas
        costo_mano_obra = random.uniform(50000, 500000)
        costo_repuestos = random.uniform(20000, 800000)
        costo_total = costo_mano_obra + costo_repuestos
        
        # Generar número de orden único
        year = fecha_ingreso.year
        existing_count = OrdenTrabajo.objects.filter(
            numero_orden__startswith=f"OT-{year}"
        ).count()
        numero_orden = f"OT-{year}-{str(existing_count + i + 1).zfill(4)}"
        
        # Verificar que el número no exista
        while OrdenTrabajo.objects.filter(numero_orden=numero_orden).exists():
            existing_count += 1
            numero_orden = f"OT-{year}-{str(existing_count + i + 1).zfill(4)}"
        
        # Descripción y trabajos
        descripcion_falla = random.choice(fallas_comunes)
        trabajos = random.choice(trabajos_realizados) if estado in ['FINALIZADO', 'ENTREGADO'] else ""
        
        # Diagnóstico
        diagnostico = f"Diagnóstico realizado para: {descripcion_falla}" if estado not in ['RECIBIDO'] else ""
        
        OrdenTrabajo.objects.create(
            numero_orden=numero_orden,
            cliente=vehiculo.cliente,
            vehiculo=vehiculo,
            fecha_ingreso=fecha_ingreso,
            fecha_estimada_entrega=fecha_estimada.date(),
            fecha_entrega_real=fecha_entrega_real,
            estado=estado,
            prioridad=random.choice(prioridades),
            kilometraje_ingreso=vehiculo.kilometraje + random.randint(100, 5000),
            descripcion_falla=descripcion_falla,
            diagnostico=diagnostico,
            trabajos_realizados=trabajos,
            costo_mano_obra=costo_mano_obra,
            costo_repuestos=costo_repuestos,
            costo_total=costo_total,
            observaciones=f"Orden para {vehiculo.marca} {vehiculo.modelo} - {vehiculo.placa}",
            created_by=created_by,
            is_active=True
        )
    
    print(f"✓ Órdenes creadas: {OrdenTrabajo.objects.count()}")

def limpiar_datos_existentes():
    """Limpiar datos de prueba existentes"""
    print("Limpiando datos existentes...")
    
    # Limpiar en orden inverso de dependencias
    OrdenTrabajo.objects.all().delete()
    Vehiculo.objects.all().delete()
    Cliente.objects.all().delete()
    # Mantener algunos usuarios base
    CustomUser.objects.exclude(username__in=['admin', 'gerente']).delete()
    
    print("✓ Datos existentes limpiados")

def main():
    """Función principal"""
    print("🚀 Iniciando población de la base de datos...")
    print("=" * 50)
    
    try:
        # Limpiar datos existentes automáticamente
        limpiar_datos_existentes()
        
        crear_usuarios()
        crear_clientes()
        crear_vehiculos()
        crear_ordenes()
        
        print("=" * 50)
        print("✅ Base de datos poblada exitosamente!")
        print(f"📊 Resumen:")
        print(f"   - Usuarios: {CustomUser.objects.count()}")
        print(f"   - Clientes: {Cliente.objects.count()}")
        print(f"   - Vehículos: {Vehiculo.objects.count()}")
        print(f"   - Órdenes: {OrdenTrabajo.objects.count()}")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error al poblar la base de datos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
