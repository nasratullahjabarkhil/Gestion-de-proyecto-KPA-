# Este diccionario asigna valores numéricos a cada tipo de respuesta del usuario
# Lo utilizo para calcular el porcentaje de cumplimiento de cada KPA
# La clave es la opción elegida ('1', '2', '3') y el valor es su ponderación

VALOR_RESPUESTA = {
    "1": 1.0,    # Cuando respondo "Sí", significa que la práctica está completamente implementada (100%)
    "2": 0.5,    # Si respondo "Parcial", indico que está a medias, solo cuenta el 50%
    "3": 0.0     # Al responder "No", significa que no está implementada, aporta 0% al cumplimiento
}