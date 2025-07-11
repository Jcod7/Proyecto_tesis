# Laboratorios de Patrones de Diseño

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

Proyecto generado el 2025-07-11 07:06:05
