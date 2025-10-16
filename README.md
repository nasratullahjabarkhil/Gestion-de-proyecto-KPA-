# 🎯 Herramienta de Diagnóstico CMMI Nivel 2


Una herramienta interactiva para evaluar el nivel de madurez de proyectos software según el modelo **CMMI (Capability Maturity Model Integration) Nivel 2**. 
Incluye dos interfaces: consola y GUI con Tkinter.

## 📋 Descripción

Esta aplicación permite evaluar proyectos de software en las **5 Áreas Clave de Proceso (KPAs)** del Nivel 2 de CMMI:

1. **Gestión de requisitos**
2. **Planificación de proyectos**
3. **Seguimiento y control de proyectos**
4. **Gestión de configuración**
5. **Aseguramiento de calidad**

El sistema evalúa cada KPA mediante preguntas específicas, calcula el nivel de cumplimiento y proporciona recomendaciones personalizadas para mejorar los procesos.

## ✨ Características

- ✅ **Evaluación completa** de las 5 KPAs del CMMI Nivel 2
- 📊 **Cálculo automático** de porcentajes de cumplimiento
- 🎯 **Recomendaciones personalizadas** según las áreas deficientes
- 🖥️ **Dos interfaces disponibles**: CLI y GUI (Tkinter)
- 📈 **Clasificación por estados**: Implementada, Parcialmente implementada, Deficiente
- 📝 **Informes detallados** con resultados y análisis
- 🔄 **Evaluación individual** o de todas las KPAs simultáneamente

## 🛠️ Requisitos

- Python 3.x
- Tkinter (incluido en la mayoría de instalaciones de Python)

## 📦 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/nasratullahjabarkhil/Gestion-de-proyecto-KPA-.git
cd Gestion-de-proyecto-KPA-
```

2. No se requieren dependencias adicionales (usa bibliotecas estándar de Python)

## 🚀 Uso

### Interfaz de Consola (CLI)

Ejecuta el script principal:

```bash
python diagnostico_cmmi_nivel2.py
```

**Opciones disponibles:**
- Evaluar todas las KPAs
- Evaluar una KPA específica
- Salir

### Interfaz Gráfica (GUI)

Ejecuta la versión con interfaz Tkinter:

```bash
python diagnostico_cmmi_tkinter.py
```

La interfaz gráfica ofrece:
- Navegación intuitiva entre KPAs
- Respuesta mediante botones de opción (Sí/Parcial/No)
- Visualización de resultados en tiempo real
- Informes completos con scroll

## 📊 Sistema de Evaluación

### Valores de Respuesta

| Respuesta | Valor | Descripción |
|-----------|-------|-------------|
| **Sí** | 1.0 | Práctica completamente implementada |
| **Parcial** | 0.5 | Práctica parcialmente implementada |
| **No** | 0.0 | Práctica no implementada |

### Clasificación por Porcentaje

| Porcentaje | Estado |
|------------|--------|
| ≥ 80% | **Implementada** |
| 50% - 79% | **Parcialmente implementada** |
| < 50% | **Deficiente** |

### Criterio de Cumplimiento Nivel 2

El proyecto cumple el **Nivel 2 de CMMI** cuando **todas las 5 KPAs** alcanzan el estado "Implementada" (≥ 80%).

## 📁 Estructura del Proyecto

```
Gestion-de-proyecto-KPA-/
│
├── diagnostico_cmmi_nivel2.py      # Interfaz de consola (CLI)
├── diagnostico_cmmi_tkinter.py     # Interfaz gráfica (GUI)
├── KPAS.py                          # Definición de las KPAs y preguntas
├── VALOR_RESPUESTA.py               # Valores numéricos de respuestas
├── RECOMENDACIONES_BASE.py          # Recomendaciones por KPA
├── porcentaje.py                    # Lógica de clasificación por estado
```

### Archivos Principales

- **`KPAS.py`**: Contiene las 5 KPAs con sus respectivas preguntas de evaluación (5 preguntas por KPA)
- **`VALOR_RESPUESTA.py`**: Define la ponderación de cada tipo de respuesta
- **`RECOMENDACIONES_BASE.py`**: Almacena recomendaciones genéricas para cada KPA
- **`porcentaje.py`**: Función para clasificar el estado según el porcentaje
- **`diagnostico_cmmi_nivel2.py`**: Aplicación completa con interfaz de consola
- **`diagnostico_cmmi_tkinter.py`**: Aplicación completa con interfaz gráfica

## 💡 Ejemplo de Uso

### Evaluación mediante CLI

```
HERRAMIENTA DIAGNÓSTICO CMMI NIVEL 2
############################################################
Opciones:
  1) Evaluar todas las KPAs (recomendado)
  2) Evaluar una KPA específica
  3) Salir
Elige una opción (1/2/3): 1

============================================================
Evaluando KPA: Gestión de requisitos
============================================================

¿Se documentan los requisitos funcionales y no funcionales?
  1) Sí
  2) Parcial
  3) No
Elige una opción (1/2/3): 1
...
```

### Salida de Ejemplo

```
INFORME RESUMIDO (todas las KPAs):
================================================================================

KPA: Gestión de requisitos
  - Cumplimiento: 90.0%
  - Estado: Implementada
  - Recomendaciones:
     - Todas las prácticas clave parecen estar satisfechas. Mantener procesos y evidencias.
...

Resumen general:
  KPAs implementadas: 4
  KPAs parcialmente implementadas: 1
  KPAs deficientes: 0

Verificación nivel 2: No cumple
Conclusión (2025-10-16 10:30:00): El proyecto NO cumple el Nivel 2 de CMMI. 
Recomendado trabajar las áreas deficientes y parciales.
```

## 🎓 Contexto Académico

Este proyecto ha sido desarrollado como parte de la asignatura **Gestión de Proyectos Software** del 3º Curso de Informática en la UCJC.

### Objetivos de Aprendizaje

- Comprender el modelo CMMI y sus niveles de madurez
- Aplicar prácticas de evaluación de procesos software
- Desarrollar herramientas de diagnóstico automatizadas
- Implementar interfaces de usuario (CLI y GUI)
- Generar informes y recomendaciones basadas en datos
