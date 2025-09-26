import datetime
import os
import json

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




    