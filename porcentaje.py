# Etiquetas por porcentaje
def estado_porcentaje(pct):
    if pct >= 80:
        return "Implementada"
    elif pct >= 50:
        return "Parcialmente implementada"
    else:
        return "Deficiente"