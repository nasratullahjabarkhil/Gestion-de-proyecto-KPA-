# Esta función clasifica el nivel de implementación según el porcentaje obtenido
# La utilizo para asignar etiquetas descriptivas a los resultados numéricos

def estado_porcentaje(pct):
    # Si el porcentaje es 80% o más, considero que la KPA está bien implementada
    if pct >= 80:
        return "Implementada"
    # Si está entre 50% y 79%, está parcialmente implementada, hay margen de mejora
    elif pct >= 50:
        return "Parcialmente implementada"
    # Si es menos del 50%, la KPA está deficiente y requiere atención urgente
    else:
        return "Deficiente"