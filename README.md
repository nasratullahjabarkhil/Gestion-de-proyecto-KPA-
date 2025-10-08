# Diagnóstico CMMI Nivel 2 — KPAs de Gestión de Proyecto

Herramienta educativa para evaluar el cumplimiento de las KPAs del Nivel 2 de CMMI en proyectos de software. Incluye:
- Interfaz de consola (CLI) interactiva
- Interfaz gráfica con Tkinter (GUI)
- Recomendaciones automáticas según respuestas


## Estructura del proyecto

- `diagnostico_cmmi_nivel2.py` — CLI principal (modular, usa los módulos locales)
- `diagnostico_cmmi_tkinter.py` — GUI con Tkinter
- `KPAS.py` — Banco de preguntas por KPA
- `VALOR_RESPUESTA.py` — Mapa de opciones a valores numéricos
- `RECOMENDACIONES_BASE.py` — Recomendaciones base por KPA
- `porcentaje.py` — Regla de clasificación por porcentaje (Implementada / Parcial / Deficiente)


## Requisitos

- Python 3.12+
- Tkinter (solo para la GUI). En macOS suele venir con el Python oficial.

No hay dependencias externas (no es necesario `pip install`).

## Uso

Desde la carpeta `PEC1` (una carpeta arriba de esta):

- CLI (consola):
```bash
python3 Gestion-de-proyecto-KPA-/diagnostico_cmmi_nivel2.py
```

- GUI (interfaz gráfica):
```bash
python3 Gestion-de-proyecto-KPA-/diagnostico_cmmi_tkinter.py
```

## Qué hace

- Plantea preguntas por cada KPA del Nivel 2 (Sí / Parcial / No)
- Calcula el porcentaje de cumplimiento por KPA y clasifica el estado
- Genera recomendaciones automáticas cuando hay respuestas Parcial/No
- Produce un resumen global (implementadas, parciales, deficientes)
- Muestra los resultados en pantalla (consola o ventana). 


## Próximas mejoras sugeridas

- Unificar el formato de respuestas entre CLI y GUI
- implementar funciones para guardar los informes.
- Añadir exportación en la GUI (botón “Guardar informe”)
- Añadir tests mínimos a la lógica (porcentaje y estado)
- Internacionalización (ES/EN)
- 

## Licencia

Uso académico