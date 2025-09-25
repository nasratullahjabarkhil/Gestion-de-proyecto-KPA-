#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diagnostico_cmmi_nivel2.py
Herramienta consola para diagnosticar CMMI Nivel 2 (práctica).
Versión: básica (V1) - Código hecho por el equipo.
Autor: Tú / Equipo
"""

import json
import datetime
import os

# ---------------------------
# CONFIG: KPAs, preguntas y recomendaciones
# ---------------------------

KPAS = {
    "Gestión de requisitos": [
        "¿Se documentan los requisitos funcionales y no funcionales?",
        "¿Existe trazabilidad entre requisitos y entregables?",
        "¿Se gestiona formalmente el cambio de requisitos?",
        "¿Se revisan los requisitos con los stakeholders?",
        "¿Se almacenan los requisitos en un repositorio accesible?"
    ],
    "Planificación de proyectos": [
        "¿Existe un plan de proyecto formalmente definido?",
        "¿Se estiman recursos y plazos de forma realista?",
        "¿Se identifican riesgos y planes de mitigación?",
        "¿Se asignan responsabilidades claramente?",
        "¿Se actualiza el plan tras cambios relevantes?"
    ],
    "Seguimiento y control de proyectos": [
        "¿Se mide el avance regularmente (métricas)?",
        "¿Se documentan desviaciones y acciones correctivas?",
        "¿Se realizan reuniones de seguimiento periódicas?",
        "¿Se gestionan problemas y decisiones formalmente?",
        "¿Se hace un reporte de estado a stakeholders?"
    ],
    "Gestión de configuración": [
        "¿Se usa control de versiones para el código?",
        "¿Se documentan releases y versiones del software?",
        "¿Existe una política de branching/merging establecida?",
        "¿Se registran cambios y motivos de cambio?",
        "¿Se mantienen artefactos (builds, entregables) controlados?"
    ],
    "Aseguramiento de calidad": [
        "¿Se definen criterios de calidad para entregas?",
        "¿Se realizan pruebas unitarias e integración sistemáticas?",
        "¿Se registran y analizan defectos?",
        "¿Se realizan revisiones y auditorías de calidad?",
        "¿Se automatizan pruebas y/o procesos de CI?"
    ]
}

# Recomendaciones por KPA (base)
RECOMENDACIONES_BASE = {
    "Gestión de requisitos": [
        "Formalizar la documentación completa de requisitos (funcionales y no funcionales).",
        "Implementar una matriz de trazabilidad entre requisitos y entregables/casos de prueba.",
        "Establecer revisiones periódicas con stakeholders para validar requisitos."
    ],
    "Planificación de proyectos": [
        "Elaborar un plan de proyecto formal: objetivos, alcance, cronograma y recursos.",
        "Incluir análisis de riesgos y planes de mitigación en la planificación.",
        "Revisar y actualizar el plan periódicamente con el equipo."
    ],
    "Seguimiento y control de proyectos": [
        "Definir métricas de avance y rendimiento (por ejemplo: porcentaje de tareas completadas).",
        "Establecer reuniones de seguimiento semanales y registrar actas.",
        "Documentar desviaciones y acciones correctivas."
    ],
    "Gestión de configuración": [
        "Adoptar control de versiones (por ejemplo Git) con una política de ramas.",
        "Documentar cambios, versiones y releases del software.",
        "Establecer una política de gestión de configuración y seguimiento de artefactos."
    ],
    "Aseguramiento de calidad": [
        "Definir criterios de calidad para cada entrega y revisar su cumplimiento.",
        "Implementar pruebas unitarias, de integración y registrar resultados.",
        "Establecer un proceso para registrar y analizar defectos y acciones correctivas."
    ]
}

# Valores numéricos para respuestas
VALOR_RESPUESTA = {
    "1": 1.0,    # Sí
    "2": 0.5,    # Parcial
    "3": 0.0     # No
}

# Etiquetas por porcentaje
def estado_porcentaje(pct):
    if pct >= 80:
        return "Implementada"
    elif pct >= 50:
        return "Parcialmente implementada"
    else:
        return "Deficiente"

# ---------------------------
# Funciones principales
# ---------------------------

def pedir_respuesta(pregunta):
    """Pide respuesta al usuario para una pregunta cerrada Sí/Parcial/No."""
    while True:
        print("\n" + pregunta)
        print("  1) Sí")
        print("  2) Parcial")
        print("  3) No")
        opcion = input("Elige una opción (1/2/3): ").strip()
        if opcion in VALOR_RESPUESTA:
            return VALOR_RESPUESTA[opcion], opcion
        print("Opción no válida. Intenta de nuevo.")

def evaluar_kpa(nombre_kpa, preguntas):
    """Realiza la evaluación interactiva para una KPA. Devuelve respuestas y metadatos."""
    print("\n" + "="*60)
    print(f"Evaluando KPA: {nombre_kpa}")
    print("="*60)
    respuestas_val = []
    respuestas_raw = []
    detalles = []  # guardamos por pregunta la opción textual
    for p in preguntas:
        val, opcion = pedir_respuesta(p)
        respuestas_val.append(val)
        respuestas_raw.append({
            "pregunta": p,
            "opcion": opcion,                # '1','2','3'
            "valor": val,
            "texto": {"1":"Sí","2":"Parcial","3":"No"}[opcion]
        })
        detalles.append({"pregunta": p, "respuesta": {"opcion": opcion, "texto": {"1":"Sí","2":"Parcial","3":"No"}[opcion], "valor": val}})
    # Calculo porcentaje
    porcentaje = (sum(respuestas_val) / len(respuestas_val)) * 100
    estado = estado_porcentaje(porcentaje)
    # recomendaciones: si hay respuestas Parcial o No, incluir recomendaciones base
    recomendaciones = generar_recomendaciones_por_respuestas(nombre_kpa, respuestas_raw)
    return {
        "kpa": nombre_kpa,
        "porcentaje": round(porcentaje, 2),
        "estado": estado,
        "detalles": detalles,
        "recomendaciones": recomendaciones,
        "respuestas_raw": respuestas_raw
    }

def generar_recomendaciones_por_respuestas(kpa, respuestas_raw):
    """
    Genera recomendaciones específicas en función de las respuestas.
    Lógica simple: si alguna respuesta es 'No' o 'Parcial', añadimos recomendaciones base.
    También podemos personalizar recomendaciones indicando qué preguntas fallan.
    """
    lista = []
    # Añadir recomendaciones base si hay problemas
    problemas = [r for r in respuestas_raw if r['opcion'] in ('2','3')]
    if problemas:
        lista.extend(RECOMENDACIONES_BASE.get(kpa, []))
        # Añadir recomendaciones concretas por pregunta fallida
        for r in problemas:
            texto_preg = r['pregunta']
            if r['opcion'] == '3':
                lista.append(f"Problema detectado: '{texto_preg}' -> No implementado. Revisar y priorizar su corrección.")
            elif r['opcion'] == '2':
                lista.append(f"Problema parcial: '{texto_preg}' -> Mejorar formalidad y consistencia.")
    else:
        lista.append("Todas las prácticas clave parecen estar satisfechas. Mantener procesos y evidencias.")
    # Evitar duplicados manteniendo orden
    seen = set()
    out = []
    for item in lista:
        if item not in seen:
            out.append(item)
            seen.add(item)
    return out

def evaluar_todas_las_kpas():
    """Evalúa interactivamente todas las KPAs y devuelve resultados en una lista."""
    resultados = []
    for kpa, preguntas in KPAS.items():
        res = evaluar_kpa(kpa, preguntas)
        resultados.append(res)
    return resultados

def diagnostico_general(resultados):
    """Calcula el diagnóstico general a partir de la lista de resultados por KPA."""
    summary = {
        "implementadas": 0,
        "parciales": 0,
        "deficientes": 0,
        "por_kpa": {}
    }
    for r in resultados:
        summary["por_kpa"][r["kpa"]] = r["porcentaje"]
        if r["estado"] == "Implementada":
            summary["implementadas"] += 1
        elif r["estado"] == "Parcialmente implementada":
            summary["parciales"] += 1
        else:
            summary["deficientes"] += 1
    # Verificación nivel 2
    cumple_nivel2 = (summary["implementadas"] == len(KPAS))
    return summary, cumple_nivel2

def recomendaciones_para_alcanzar_nivel2(resultados):
    """
    Genera recomendaciones generales para alcanzar el Nivel 2:
    se agrupan las recomendaciones por KPA que no estén implementadas.
    """
    recomendaciones = []
    for r in resultados:
        if r["estado"] != "Implementada":
            recomendaciones.append({
                "kpa": r["kpa"],
                "estado": r["estado"],
                "recomendaciones": r["recomendaciones"]
            })
    if not recomendaciones:
        return ["El proyecto cumple los requisitos de Nivel 2. Mantener las prácticas actuales."]
    return recomendaciones

def conclusion_final(cumple_nivel2, summary):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if cumple_nivel2:
        msg = f"Conclusión ({now}): El proyecto cumple el Nivel 2 de CMMI."
    else:
        msg = f"Conclusión ({now}): El proyecto NO cumple el Nivel 2 de CMMI. Recomendado trabajar las áreas deficientes y parciales."
    return msg

# ---------------------------
# Funciones de export / helpers
# ---------------------------

def generar_informe_text(project_name, resultados, summary, cumple_nivel2):
    """Genera texto legible del informe completo."""
    lines = []
    lines.append(f"Diagnóstico CMMI Nivel 2 - Proyecto: {project_name}")
    lines.append(f"Fecha: {datetime.datetime.now().isoformat()}")
    lines.append("="*80)
    for r in resultados:
        lines.append(f"\nKPA: {r['kpa']}")
        lines.append(f"  - Porcentaje de cumplimiento: {r['porcentaje']}%")
        lines.append(f"  - Estado: {r['estado']}")
        lines.append("  - Respuestas:")
        for d in r['detalles']:
            lines.append(f"     * {d['pregunta']} -> {d['respuesta']['texto']}")
        lines.append("  - Recomendaciones:")
        for rec in r['recomendaciones']:
            lines.append(f"     - {rec}")
    lines.append("\n" + "="*80)
    lines.append("\nResumen general:")
    lines.append(f"  KPAs implementadas: {summary['implementadas']}")
    lines.append(f"  KPAs parcialmente implementadas: {summary['parciales']}")
    lines.append(f"  KPAs deficientes: {summary['deficientes']}")
    lines.append(f"\nVerificación nivel 2: {'Cumple' if cumple_nivel2 else 'No cumple'}")
    lines.append("\nConclusión:")
    lines.append(conclusion_final(cumple_nivel2, summary))
    return "\n".join(lines)

def exportar_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Informe JSON guardado en: {path}")

def exportar_txt(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Informe TXT guardado en: {path}")

# ---------------------------
# INTERFAZ CONSOLA - FLUJO PRINCIPAL
# ---------------------------

def menu_principal():
    print("\n" + "#"*60)
    print("HERRAMIENTA DIAGNÓSTICO CMMI NIVEL 2")
    print("#"*60)
    print("Opciones:")
    print("  1) Evaluar todas las KPAs (recomendado)")
    print("  2) Evaluar una KPA específica")
    print("  3) Salir")
    opcion = input("Elige una opción (1/2/3): ").strip()
    return opcion

def elegir_kpa():
    print("\nSelecciona la KPA a evaluar:")
    kpas = list(KPAS.keys())
    for i, k in enumerate(kpas, start=1):
        print(f"  {i}) {k}")
    while True:
        op = input(f"Elige (1-{len(kpas)}): ").strip()
        if op.isdigit() and 1 <= int(op) <= len(kpas):
            return kpas[int(op)-1]
        print("Opción no válida.")

def guardar_informes(project_name, resultados, summary, cumple_nivel2):
    # Carpeta de salida
    folder = f"informes_{project_name.replace(' ', '_')}"
    os.makedirs(folder, exist_ok=True)
    # JSON (estructura completa)
    data = {
        "proyecto": project_name,
        "fecha": datetime.datetime.now().isoformat(),
        "resultados": resultados,
        "resumen": summary,
        "cumple_nivel2": cumple_nivel2
    }
    json_path = os.path.join(folder, "informe_completo.json")
    exportar_json(json_path, data)
    # TXT (legible)
    txt_path = os.path.join(folder, "informe_legible.txt")
    texto = generar_informe_text(project_name, resultados, summary, cumple_nivel2)
    exportar_txt(txt_path, texto)
    print(f"Informes guardados en la carpeta: {folder}")

def main():
    print("Bienvenido a la herramienta de diagnóstico CMMI Nivel 2.")
    project_name = input("Nombre del proyecto: ").strip()
    if project_name == "":
        project_name = "Proyecto_sin_nombre"

    while True:
        opcion = menu_principal()
        if opcion == "1":
            resultados = evaluar_todas_las_kpas()
            summary, cumple_nivel2 = diagnostico_general(resultados)
            texto = generar_informe_text(project_name, resultados, summary, cumple_nivel2)
            print("\n" + "="*80)
            print("INFORME RESUMIDO:")
            print("="*80)
            print(texto)
            # Guardar archivos
            guardar = input("\n¿Deseas exportar el informe a archivos (JSON/TXT)? (s/n): ").strip().lower()
            if guardar == "s":
                guardar_informes(project_name, resultados, summary, cumple_nivel2)
            else:
                print("No se han guardado archivos.")
            # Tras una evaluación completa, salimos o permitimos nueva ejecución
            repetir = input("\n¿Quieres realizar otra evaluación? (s/n): ").strip().lower()
            if repetir != "s":
                print("Fin. ¡Buena suerte con la práctica!")
                break

        elif opcion == "2":
            kpa = elegir_kpa()
            res = evaluar_kpa(kpa, KPAS[kpa])
            resultados = [res]
            summary, cumple_nivel2 = diagnostico_general(resultados)
            texto = generar_informe_text(project_name, resultados, summary, cumple_nivel2)
            print("\n" + "="*60)
            print("Informe KPA seleccionado:")
            print("="*60)
            print(texto)
            guardar = input("\n¿Deseas exportar este informe (JSON/TXT)? (s/n): ").strip().lower()
            if guardar == "s":
                guardar_informes(project_name, resultados, summary, cumple_nivel2)
            repetir = input("\n¿Quieres evaluar otra KPA o volver al menú principal? (v=volver, s=salir): ").strip().lower()
            if repetir == "s":
                print("Fin. ¡Buena suerte con la práctica!")
                break
            # si vuelve, continúa el bucle

        elif opcion == "3":
            print("Saliendo. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
