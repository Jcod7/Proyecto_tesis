#!/usr/bin/env python3
"""
Script de Instalación y Configuración
Prepara el entorno para ejecutar todos los laboratorios
"""

import os
import subprocess
import sys
from datetime import datetime

class InstaladorLaboratorios:
    def __init__(self):
        self.dependencias = [
            'matplotlib>=3.5.0',
            'pandas>=1.3.0',
            'numpy>=1.21.0',
            'scipy>=1.7.0',
            'seaborn>=0.11.0',
            'requests>=2.25.0',
            'psutil>=5.8.0',
            'radon>=5.1.0',
            'lizard>=1.17.0'
        ]
        
    def verificar_python(self):
        """Verifica versión de Python"""
        print("=== VERIFICACIÓN DE PYTHON ===")
        version = sys.version_info
        print(f"Python version: {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Error: Se requiere Python 3.8 o superior")
            return False
        
        print("✅ Versión de Python compatible")
        return True
    
    def verificar_django(self):
        """Verifica instalación de Django"""
        print("\n=== VERIFICACIÓN DE DJANGO ===")
        try:
            import django
            print(f"Django version: {django.get_version()}")
            
            # Verificar si es compatible
            version_parts = django.get_version().split('.')
            major = int(version_parts[0])
            minor = int(version_parts[1])
            
            if major < 4 or (major == 4 and minor < 2):
                print("⚠️  Advertencia: Se recomienda Django 4.2+ para mejor compatibilidad")
            
            print("✅ Django instalado")
            return True
        except ImportError:
            print("❌ Django no está instalado")
            return False
    
    def instalar_dependencias(self):
        """Instala dependencias necesarias"""
        print("\n=== INSTALACIÓN DE DEPENDENCIAS ===")
        
        for dep in self.dependencias:
            print(f"Instalando {dep}...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                             check=True, capture_output=True)
                print(f"✅ {dep} instalado")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error instalando {dep}: {e}")
                return False
        
        print("✅ Todas las dependencias instaladas")
        return True
    
    def verificar_estructura_proyecto(self):
        """Verifica estructura del proyecto"""
        print("\n=== VERIFICACIÓN DE ESTRUCTURA ===")
        
        archivos_necesarios = [
            'patron_mvc/manage.py',
            'patron_mvc/apps/accounts/models.py',
            'patron_mvc/apps/clientes/models.py',
            'patron_mvc/apps/vehiculos/models.py',
            'patron_mvc/apps/ordenes/models.py',
            'patron_mvc/db.sqlite3'
        ]
        
        todos_ok = True
        for archivo in archivos_necesarios:
            if os.path.exists(archivo):
                print(f"✅ {archivo}")
            else:
                print(f"❌ {archivo} no encontrado")
                todos_ok = False
        
        if not todos_ok:
            print("⚠️  Algunos archivos del proyecto faltan")
            return False
        
        print("✅ Estructura del proyecto correcta")
        return True
    
    def crear_directorios(self):
        """Crea directorios necesarios"""
        print("\n=== CREACIÓN DE DIRECTORIOS ===")
        
        directorios = [
            'resultados',
            'laboratorios',
            'docs'
        ]
        
        for dir_name in directorios:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
                print(f"✅ Creado directorio: {dir_name}")
            else:
                print(f"✅ Directorio existente: {dir_name}")
    
    def verificar_servidor_django(self):
        """Verifica que el servidor Django puede iniciarse"""
        print("\n=== VERIFICACIÓN DEL SERVIDOR DJANGO ===")
        
        try:
            # Cambiar al directorio del proyecto
            os.chdir('patron_mvc')
            
            # Verificar migrations
            print("Verificando migraciones...")
            result = subprocess.run([sys.executable, 'manage.py', 'showmigrations'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Migraciones verificadas")
            else:
                print("⚠️  Problemas con migraciones")
                print(result.stderr)
            
            # Verificar que el servidor puede iniciarse (check)
            print("Verificando configuración del servidor...")
            result = subprocess.run([sys.executable, 'manage.py', 'check'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Servidor Django configurado correctamente")
                return True
            else:
                print("❌ Problemas con configuración del servidor")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error verificando servidor: {e}")
            return False
        finally:
            os.chdir('..')
    
    def crear_archivo_requirements(self):
        """Crea archivo requirements.txt"""
        print("\n=== CREACIÓN DE REQUIREMENTS.TXT ===")
        
        requirements_content = """# Dependencias del proyecto
Django>=4.2.0
matplotlib>=3.5.0
pandas>=1.3.0
numpy>=1.21.0
scipy>=1.7.0
seaborn>=0.11.0
requests>=2.25.0
psutil>=5.8.0
radon>=5.1.0
lizard>=1.17.0

# Dependencias adicionales
python-dateutil>=2.8.0
pillow>=8.0.0
"""
        
        with open('requirements.txt', 'w') as f:
            f.write(requirements_content)
        
        print("✅ requirements.txt creado")
    
    def crear_documentacion(self):
        """Crea documentación básica"""
        print("\n=== CREACIÓN DE DOCUMENTACIÓN ===")
        
        readme_content = f"""# Laboratorios de Patrones de Diseño

## Descripción
Este proyecto implementa laboratorios para evaluar patrones de diseño en arquitecturas monolíticas vs microservicios.

## Instalación

### 1. Requisitos Previos
- Python 3.8+
- Django 4.2+
- 8GB RAM disponible
- 5GB espacio en disco

### 2. Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configuración de la Base de Datos
```bash
cd patron_mvc
python manage.py migrate
python poblar_db.py
```

## Ejecución de Laboratorios

### Laboratorio 1: Análisis de Rendimiento
```bash
# Iniciar servidor Django
python manage.py runserver 8002 &

# Ejecutar análisis de rendimiento
python laboratorio_rendimiento.py
```

### Laboratorio 2-4: Análisis de Patrones
```bash
python laboratorios_especificos.py
```

### Análisis Estadístico Completo
```bash
python script_analisis.py
```

## Resultados

Los resultados se guardan en la carpeta `resultados/`:
- `rendimiento_resultados.csv` - Métricas de rendimiento
- `patrones_resultados.json` - Análisis de patrones
- `analisis_rendimiento_completo.png` - Gráficos de rendimiento
- `analisis_patrones_completo.png` - Gráficos de patrones
- `reporte_consolidado.html` - Reporte final HTML
- `reporte_consolidado.txt` - Reporte final texto

## Estructura del Proyecto

```
proyecto_tesis/
├── patron_mvc/                    # Sistema Django monolítico
├── laboratorio_rendimiento.py     # Lab 1: Rendimiento
├── laboratorios_especificos.py    # Labs 2-4: Patrones específicos
├── script_analisis.py             # Análisis estadístico
├── setup_laboratorios.py          # Configuración inicial
├── requirements.txt               # Dependencias
└── resultados/                    # Carpeta de resultados
```

## Contacto

Proyecto generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ README.md creado")
    
    def ejecutar_configuracion_completa(self):
        """Ejecuta configuración completa del entorno"""
        print("=== CONFIGURACIÓN COMPLETA DEL ENTORNO ===")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        pasos = [
            ("Verificar Python", self.verificar_python),
            ("Verificar Django", self.verificar_django),
            ("Instalar dependencias", self.instalar_dependencias),
            ("Verificar estructura", self.verificar_estructura_proyecto),
            ("Crear directorios", self.crear_directorios),
            ("Verificar servidor Django", self.verificar_servidor_django),
            ("Crear requirements.txt", self.crear_archivo_requirements),
            ("Crear documentación", self.crear_documentacion)
        ]
        
        resultados = []
        for descripcion, funcion in pasos:
            print(f"\n{descripcion}...")
            try:
                resultado = funcion()
                resultados.append((descripcion, resultado))
                if resultado:
                    print(f"✅ {descripcion} completado")
                else:
                    print(f"❌ {descripcion} falló")
            except Exception as e:
                print(f"❌ Error en {descripcion}: {e}")
                resultados.append((descripcion, False))
        
        # Resumen final
        print("\n=== RESUMEN DE CONFIGURACIÓN ===")
        exitos = sum(1 for _, resultado in resultados if resultado)
        total = len(resultados)
        
        print(f"Pasos completados: {exitos}/{total}")
        
        if exitos == total:
            print("🎉 ¡Configuración completada exitosamente!")
            print("\nPróximos pasos:")
            print("1. cd patron_mvc")
            print("2. python manage.py runserver 8002 &")
            print("3. python ../laboratorio_rendimiento.py")
            print("4. python ../laboratorios_especificos.py")
            print("5. python ../script_analisis.py")
        else:
            print("⚠️  Algunos pasos fallaron. Revise los errores anteriores.")
            
            print("\nPasos fallidos:")
            for descripcion, resultado in resultados:
                if not resultado:
                    print(f"- {descripcion}")
        
        return exitos == total

if __name__ == "__main__":
    instalador = InstaladorLaboratorios()
    
    print("🚀 Iniciando configuración del entorno para laboratorios...")
    exito = instalador.ejecutar_configuracion_completa()
    
    if exito:
        print("\n🎯 El entorno está listo para ejecutar los laboratorios!")
    else:
        print("\n❌ La configuración no se completó correctamente.")
        print("   Revise los errores y ejecute nuevamente.")
