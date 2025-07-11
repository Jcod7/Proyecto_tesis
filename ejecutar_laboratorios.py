#!/usr/bin/env python3
"""
Script de Ejecución Completa
Ejecuta todos los laboratorios en secuencia
"""

import os
import sys
import time
import subprocess
import threading
from datetime import datetime

class EjecutorLaboratorios:
    def __init__(self):
        self.servidor_proceso = None
        self.servidor_pid = None
        
    def iniciar_servidor_django(self):
        """Inicia servidor Django en background"""
        print("=== INICIANDO SERVIDOR DJANGO ===")
        
        try:
            os.chdir('patron_mvc')
            
            # Verificar que el servidor no esté corriendo
            self.detener_servidor_existente()
            
            # Iniciar servidor
            self.servidor_proceso = subprocess.Popen([
                sys.executable, 'manage.py', 'runserver', '8002'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Esperar a que el servidor inicie
            print("Esperando a que el servidor inicie...")
            time.sleep(10)
            
            # Verificar que el servidor esté corriendo
            if self.servidor_proceso.poll() is None:
                print("✅ Servidor Django iniciado en puerto 8002")
                return True
            else:
                print("❌ Error iniciando servidor Django")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando servidor: {e}")
            return False
        finally:
            os.chdir('..')
    
    def detener_servidor_existente(self):
        """Detiene servidor existente si está corriendo"""
        try:
            # Intentar encontrar y terminar proceso en puerto 8002
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['cmdline'] and 'runserver' in ' '.join(proc.info['cmdline']):
                        if '8002' in ' '.join(proc.info['cmdline']):
                            proc.terminate()
                            proc.wait(timeout=5)
                            print(f"✅ Proceso Django terminado: {proc.info['pid']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except ImportError:
            # Si psutil no está disponible, continuar
            pass
    
    def detener_servidor_django(self):
        """Detiene servidor Django"""
        if self.servidor_proceso:
            print("Deteniendo servidor Django...")
            self.servidor_proceso.terminate()
            try:
                self.servidor_proceso.wait(timeout=5)
                print("✅ Servidor Django detenido")
            except subprocess.TimeoutExpired:
                self.servidor_proceso.kill()
                print("✅ Servidor Django terminado forzadamente")
    
    def ejecutar_laboratorio_rendimiento(self):
        """Ejecuta laboratorio de rendimiento"""
        print("\n=== EJECUTANDO LABORATORIO DE RENDIMIENTO ===")
        
        try:
            # Verificar que el servidor esté disponible
            import requests
            response = requests.get("http://localhost:8002/", timeout=5)
            if response.status_code != 200:
                print("❌ Servidor no disponible")
                return False
        except Exception as e:
            print(f"❌ Error conectando al servidor: {e}")
            return False
        
        try:
            result = subprocess.run([
                sys.executable, 'laboratorio_rendimiento.py'
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ Laboratorio de rendimiento completado")
                print(result.stdout)
                return True
            else:
                print("❌ Error en laboratorio de rendimiento")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout en laboratorio de rendimiento")
            return False
        except Exception as e:
            print(f"❌ Error ejecutando laboratorio: {e}")
            return False
    
    def ejecutar_laboratorios_patrones(self):
        """Ejecuta laboratorios de patrones específicos"""
        print("\n=== EJECUTANDO LABORATORIOS DE PATRONES ===")
        
        try:
            result = subprocess.run([
                sys.executable, 'laboratorios_especificos.py'
            ], capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                print("✅ Laboratorios de patrones completados")
                print(result.stdout)
                return True
            else:
                print("❌ Error en laboratorios de patrones")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout en laboratorios de patrones")
            return False
        except Exception as e:
            print(f"❌ Error ejecutando laboratorios: {e}")
            return False
    
    def ejecutar_analisis_estadistico(self):
        """Ejecuta análisis estadístico"""
        print("\n=== EJECUTANDO ANÁLISIS ESTADÍSTICO ===")
        
        try:
            result = subprocess.run([
                sys.executable, 'script_analisis.py'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ Análisis estadístico completado")
                print(result.stdout)
                return True
            else:
                print("❌ Error en análisis estadístico")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout en análisis estadístico")
            return False
        except Exception as e:
            print(f"❌ Error ejecutando análisis: {e}")
            return False
    
    def verificar_dependencias(self):
        """Verifica que todas las dependencias estén instaladas"""
        print("=== VERIFICANDO DEPENDENCIAS ===")
        
        dependencias = [
            'django',
            'matplotlib',
            'pandas',
            'numpy',
            'scipy',
            'requests',
            'psutil'
        ]
        
        faltantes = []
        for dep in dependencias:
            try:
                __import__(dep)
                print(f"✅ {dep}")
            except ImportError:
                print(f"❌ {dep} no encontrado")
                faltantes.append(dep)
        
        if faltantes:
            print(f"\n❌ Dependencias faltantes: {', '.join(faltantes)}")
            print("Ejecute: pip install " + " ".join(faltantes))
            return False
        
        print("✅ Todas las dependencias están instaladas")
        return True
    
    def verificar_archivos_laboratorio(self):
        """Verifica que todos los archivos de laboratorio existan"""
        print("\n=== VERIFICANDO ARCHIVOS DE LABORATORIO ===")
        
        archivos = [
            'laboratorio_rendimiento.py',
            'laboratorios_especificos.py',
            'script_analisis.py',
            'patron_mvc/manage.py'
        ]
        
        faltantes = []
        for archivo in archivos:
            if os.path.exists(archivo):
                print(f"✅ {archivo}")
            else:
                print(f"❌ {archivo} no encontrado")
                faltantes.append(archivo)
        
        if faltantes:
            print(f"\n❌ Archivos faltantes: {', '.join(faltantes)}")
            return False
        
        print("✅ Todos los archivos de laboratorio están disponibles")
        return True
    
    def crear_backup_resultados(self):
        """Crea backup de resultados anteriores"""
        if os.path.exists('resultados'):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = f'resultados_backup_{timestamp}'
            
            try:
                import shutil
                shutil.copytree('resultados', backup_dir)
                print(f"✅ Backup creado: {backup_dir}")
            except Exception as e:
                print(f"⚠️  No se pudo crear backup: {e}")
    
    def mostrar_resumen_resultados(self):
        """Muestra resumen de resultados generados"""
        print("\n=== RESUMEN DE RESULTADOS ===")
        
        archivos_esperados = [
            'resultados/rendimiento_resultados.csv',
            'resultados/patrones_resultados.json',
            'resultados/analisis_rendimiento_completo.png',
            'resultados/analisis_patrones_completo.png',
            'resultados/reporte_consolidado.html',
            'resultados/reporte_consolidado.txt'
        ]
        
        archivos_generados = []
        for archivo in archivos_esperados:
            if os.path.exists(archivo):
                size = os.path.getsize(archivo)
                print(f"✅ {archivo} ({size} bytes)")
                archivos_generados.append(archivo)
            else:
                print(f"❌ {archivo} no generado")
        
        print(f"\nArchivos generados: {len(archivos_generados)}/{len(archivos_esperados)}")
        
        if len(archivos_generados) == len(archivos_esperados):
            print("🎉 ¡Todos los resultados generados exitosamente!")
            print("\nPuede revisar:")
            print("- resultados/reporte_consolidado.html (navegador)")
            print("- resultados/reporte_consolidado.txt (texto)")
            print("- resultados/*.png (gráficos)")
        else:
            print("⚠️  Algunos resultados no fueron generados")
    
    def ejecutar_suite_completa(self):
        """Ejecuta suite completa de laboratorios"""
        print("🚀 EJECUCIÓN COMPLETA DE LABORATORIOS")
        print("=" * 50)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Registro de tiempo
        tiempo_inicio = time.time()
        
        # Crear backup de resultados anteriores
        self.crear_backup_resultados()
        
        # Verificaciones previas
        if not self.verificar_dependencias():
            return False
        
        if not self.verificar_archivos_laboratorio():
            return False
        
        # Secuencia de ejecución
        pasos = [
            ("Iniciar servidor Django", self.iniciar_servidor_django),
            ("Ejecutar laboratorio de rendimiento", self.ejecutar_laboratorio_rendimiento),
            ("Ejecutar laboratorios de patrones", self.ejecutar_laboratorios_patrones),
            ("Ejecutar análisis estadístico", self.ejecutar_analisis_estadistico)
        ]
        
        resultados = []
        
        try:
            for descripcion, funcion in pasos:
                print(f"\n{descripcion}...")
                resultado = funcion()
                resultados.append((descripcion, resultado))
                
                if not resultado:
                    print(f"❌ {descripcion} falló. Abortando ejecución.")
                    break
                    
                print(f"✅ {descripcion} completado")
        
        except KeyboardInterrupt:
            print("\n⚠️  Ejecución interrumpida por el usuario")
            return False
        
        finally:
            # Siempre detener el servidor
            self.detener_servidor_django()
        
        # Calcular tiempo total
        tiempo_total = time.time() - tiempo_inicio
        
        # Mostrar resumen
        print("\n" + "=" * 50)
        print("RESUMEN DE EJECUCIÓN")
        print("=" * 50)
        
        exitos = sum(1 for _, resultado in resultados if resultado)
        total = len(resultados)
        
        print(f"Pasos completados: {exitos}/{total}")
        print(f"Tiempo total: {tiempo_total:.1f} segundos")
        
        for descripcion, resultado in resultados:
            estado = "✅" if resultado else "❌"
            print(f"{estado} {descripcion}")
        
        if exitos == total:
            print("\n🎉 ¡LABORATORIOS COMPLETADOS EXITOSAMENTE!")
            self.mostrar_resumen_resultados()
            
            print("\n📊 PRÓXIMOS PASOS:")
            print("1. Revisar reporte consolidado en resultados/reporte_consolidado.html")
            print("2. Analizar gráficos en resultados/*.png")
            print("3. Revisar métricas detalladas en archivos CSV/JSON")
            
            return True
        else:
            print("\n❌ ALGUNOS LABORATORIOS FALLARON")
            print("Revise los errores anteriores y ejecute nuevamente")
            return False

if __name__ == "__main__":
    print("🎯 Iniciando ejecución completa de laboratorios...")
    print("   Esto puede tomar varios minutos...")
    print("   Presione Ctrl+C para cancelar en cualquier momento")
    print()
    
    # Preguntar confirmación
    respuesta = input("¿Continuar con la ejecución? (s/N): ").strip().lower()
    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("Ejecución cancelada por el usuario")
        sys.exit(0)
    
    ejecutor = EjecutorLaboratorios()
    exito = ejecutor.ejecutar_suite_completa()
    
    if exito:
        print("\n🎉 ¡Ejecución completada exitosamente!")
        sys.exit(0)
    else:
        print("\n❌ La ejecución no se completó correctamente")
        sys.exit(1)
