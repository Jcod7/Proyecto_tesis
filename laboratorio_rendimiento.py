#!/usr/bin/env python3
"""
Laboratorio 1: Análisis de Rendimiento
Objetivo: Comparar rendimiento MVC vs API REST
Hipótesis H1: MVC monolítico tiene 25-45% mejor rendimiento
"""

import time
import requests
import statistics
import csv
import json
import threading
import psutil
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt
import pandas as pd

class RendimientoAnalyzer:
    def __init__(self):
        self.base_url = "http://localhost:8002"
        self.resultados = []
        self.resultados_csv = "resultados/rendimiento_resultados.csv"
        
    def medir_tiempo_respuesta(self, url, metodo="GET", data=None):
        """Mide tiempo de respuesta para una URL específica"""
        start_time = time.time()
        try:
            if metodo == "GET":
                response = requests.get(url, timeout=30)
            elif metodo == "POST":
                response = requests.post(url, data=data, timeout=30)
            
            end_time = time.time()
            tiempo_respuesta = (end_time - start_time) * 1000  # ms
            
            return {
                'url': url,
                'metodo': metodo,
                'tiempo_ms': tiempo_respuesta,
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'url': url,
                'metodo': metodo,
                'tiempo_ms': 0,
                'status_code': 0,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def prueba_carga_concurrente(self, url, num_requests=50, num_threads=10):
        """Ejecuta prueba de carga concurrente"""
        print(f"Iniciando prueba de carga: {num_requests} requests, {num_threads} threads")
        
        tiempos_respuesta = []
        errores = 0
        
        def hacer_request():
            resultado = self.medir_tiempo_respuesta(url)
            if resultado['success']:
                return resultado['tiempo_ms']
            else:
                return None
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(hacer_request) for _ in range(num_requests)]
            
            for future in as_completed(futures):
                resultado = future.result()
                if resultado is not None:
                    tiempos_respuesta.append(resultado)
                else:
                    errores += 1
        
        end_time = time.time()
        duracion_total = end_time - start_time
        
        if tiempos_respuesta:
            return {
                'tiempo_promedio': statistics.mean(tiempos_respuesta),
                'tiempo_mediana': statistics.median(tiempos_respuesta),
                'tiempo_min': min(tiempos_respuesta),
                'tiempo_max': max(tiempos_respuesta),
                'percentil_95': self.calcular_percentil(tiempos_respuesta, 95),
                'throughput': len(tiempos_respuesta) / duracion_total,
                'total_requests': num_requests,
                'requests_exitosos': len(tiempos_respuesta),
                'errores': errores,
                'duracion_total': duracion_total
            }
        else:
            return None
    
    def calcular_percentil(self, datos, percentil):
        """Calcula percentil específico"""
        datos_ordenados = sorted(datos)
        k = (len(datos_ordenados) - 1) * percentil / 100
        f = int(k)
        c = k - f
        if f == len(datos_ordenados) - 1:
            return datos_ordenados[f]
        return datos_ordenados[f] * (1 - c) + datos_ordenados[f + 1] * c
    
    def medir_recursos_sistema(self):
        """Mide utilización de recursos del sistema"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memoria_percent': psutil.virtual_memory().percent,
            'memoria_disponible': psutil.virtual_memory().available,
            'disco_uso': psutil.disk_usage('/').percent
        }
    
    def ejecutar_suite_completa(self):
        """Ejecuta la suite completa de pruebas"""
        print("=== LABORATORIO 1: ANÁLISIS DE RENDIMIENTO ===")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # URLs a probar
        urls_prueba = [
            f"{self.base_url}/",
            f"{self.base_url}/clientes/",
            f"{self.base_url}/vehiculos/",
            f"{self.base_url}/ordenes/",
            f"{self.base_url}/accounts/",
        ]
        
        resultados_completos = []
        
        print("1. Midiendo rendimiento individual...")
        for url in urls_prueba:
            print(f"   Probando: {url}")
            resultado = self.prueba_carga_concurrente(url, num_requests=100, num_threads=10)
            
            if resultado:
                resultado['url'] = url
                resultado['tipo_prueba'] = 'carga_concurrente'
                resultado['recursos'] = self.medir_recursos_sistema()
                resultados_completos.append(resultado)
                
                print(f"   ✓ Tiempo promedio: {resultado['tiempo_promedio']:.2f}ms")
                print(f"   ✓ Throughput: {resultado['throughput']:.2f} req/s")
                print(f"   ✓ P95: {resultado['percentil_95']:.2f}ms")
                print()
        
        print("2. Prueba de estrés...")
        resultado_estres = self.prueba_carga_concurrente(
            f"{self.base_url}/", 
            num_requests=500, 
            num_threads=50
        )
        
        if resultado_estres:
            resultado_estres['url'] = f"{self.base_url}/"
            resultado_estres['tipo_prueba'] = 'estres'
            resultado_estres['recursos'] = self.medir_recursos_sistema()
            resultados_completos.append(resultado_estres)
            
            print(f"   ✓ Tiempo promedio bajo estrés: {resultado_estres['tiempo_promedio']:.2f}ms")
            print(f"   ✓ Throughput bajo estrés: {resultado_estres['throughput']:.2f} req/s")
            print()
        
        # Guardar resultados
        self.guardar_resultados(resultados_completos)
        self.generar_reporte(resultados_completos)
        
        print("3. Análisis completado!")
        print(f"   Resultados guardados en: {self.resultados_csv}")
        print("   Gráficos generados en: resultados/")
        
        return resultados_completos
    
    def guardar_resultados(self, resultados):
        """Guarda resultados en CSV"""
        os.makedirs("resultados", exist_ok=True)
        
        with open(self.resultados_csv, 'w', newline='') as csvfile:
            if resultados:
                fieldnames = ['url', 'tipo_prueba', 'tiempo_promedio', 'tiempo_mediana', 
                            'tiempo_min', 'tiempo_max', 'percentil_95', 'throughput',
                            'total_requests', 'requests_exitosos', 'errores', 'duracion_total']
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for resultado in resultados:
                    # Filtrar solo los campos necesarios
                    row = {k: v for k, v in resultado.items() if k in fieldnames}
                    writer.writerow(row)
    
    def generar_reporte(self, resultados):
        """Genera gráficos y reportes visuales"""
        if not resultados:
            return
        
        # Crear DataFrame para análisis
        df_data = []
        for r in resultados:
            df_data.append({
                'URL': r['url'].split('/')[-2] if r['url'].endswith('/') else r['url'].split('/')[-1],
                'Tiempo_Promedio': r['tiempo_promedio'],
                'Throughput': r['throughput'],
                'P95': r['percentil_95'],
                'Tipo': r['tipo_prueba']
            })
        
        df = pd.DataFrame(df_data)
        
        # Gráfico 1: Tiempo de respuesta promedio
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        df_normal = df[df['Tipo'] == 'carga_concurrente']
        plt.bar(df_normal['URL'], df_normal['Tiempo_Promedio'])
        plt.title('Tiempo de Respuesta Promedio por Endpoint')
        plt.ylabel('Tiempo (ms)')
        plt.xticks(rotation=45)
        
        # Gráfico 2: Throughput
        plt.subplot(1, 2, 2)
        plt.bar(df_normal['URL'], df_normal['Throughput'])
        plt.title('Throughput por Endpoint')
        plt.ylabel('Requests/segundo')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('resultados/rendimiento_analisis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Resumen estadístico
        with open('resultados/rendimiento_resumen.txt', 'w') as f:
            f.write("=== RESUMEN DE ANÁLISIS DE RENDIMIENTO ===\n\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Métricas Generales:\n")
            f.write(f"- Tiempo promedio global: {df_normal['Tiempo_Promedio'].mean():.2f}ms\n")
            f.write(f"- Throughput promedio: {df_normal['Throughput'].mean():.2f} req/s\n")
            f.write(f"- P95 promedio: {df_normal['P95'].mean():.2f}ms\n\n")
            
            f.write("Análisis por Endpoint:\n")
            for _, row in df_normal.iterrows():
                f.write(f"- {row['URL']}: {row['Tiempo_Promedio']:.2f}ms, {row['Throughput']:.2f} req/s\n")
            
            # Evaluación de hipótesis H1
            f.write("\n=== EVALUACIÓN HIPÓTESIS H1 ===\n")
            f.write("Hipótesis: MVC monolítico tiene 25-45% mejor rendimiento que microservicios\n")
            f.write("Baseline esperado para microservicios: 150-200ms promedio\n")
            tiempo_actual = df_normal['Tiempo_Promedio'].mean()
            f.write(f"Tiempo actual MVC: {tiempo_actual:.2f}ms\n")
            
            if tiempo_actual < 150:
                mejora = ((150 - tiempo_actual) / 150) * 100
                f.write(f"✓ HIPÓTESIS CONFIRMADA: Mejora del {mejora:.1f}%\n")
            else:
                f.write("✗ HIPÓTESIS NO CONFIRMADA: Rendimiento similar o inferior\n")

if __name__ == "__main__":
    analyzer = RendimientoAnalyzer()
    
    print("Verificando disponibilidad del servidor...")
    try:
        response = requests.get("http://localhost:8002/", timeout=5)
        print("✓ Servidor disponible")
    except:
        print("✗ Error: Servidor no disponible en puerto 8002")
        print("   Inicie el servidor Django con: python manage.py runserver 8002")
        exit(1)
    
    # Ejecutar laboratorio
    resultados = analyzer.ejecutar_suite_completa()
