# Importo las librerías y módulos necesarios para mi herramienta de diagnóstico CMMI
import datetime  # Lo necesito para registrar fecha y hora en la conclusión final
from KPAS import KPAS  # Cargo las 5 KPAs con sus preguntas
from VALOR_RESPUESTA import VALOR_RESPUESTA  # Importo los valores numéricos de cada respuesta
from RECOMENDACIONES_BASE import RECOMENDACIONES_BASE  # Traigo las recomendaciones generales
from porcentaje import estado_porcentaje  # Función para clasificar según el porcentaje


def respuesta_usuario(pregunta):
    """
    Esta función la uso para hacer una pregunta al usuario y obtener su respuesta.
    Valido que la respuesta sea correcta (1, 2 o 3) y si no, pido que vuelva a intentarlo.
    Devuelvo tanto el valor numérico como la opción seleccionada.
    """
    while True:  # Creo un bucle infinito hasta que obtenga una respuesta válida
        print("\n" + pregunta)  # Muestro la pregunta
        print("  1) Sí")  # Primera opción: práctica completamente implementada
        print("  2) Parcial")  # Segunda opción: implementación parcial
        print("  3) No")  # Tercera opción: no implementada
        opcion = input("Elige una opción (1/2/3): ").strip()  # Leo la respuesta y elimino espacios
        
        # Verifico si la opción está en mi diccionario VALOR_RESPUESTA
        if opcion in VALOR_RESPUESTA:
            # Si es válida, devuelvo el valor numérico y la opción seleccionada
            return VALOR_RESPUESTA[opcion], opcion
        
        # Si la opción no es válida, muestro un mensaje de error y vuelvo a preguntar
        print("Opción no válida. Intenta de nuevo.")

def evaluar_kpa(nombre_kpa, preguntas):
    """
    Esta es mi función principal para evaluar una KPA completa.
    Recibo el nombre de la KPA y su lista de preguntas, hago todas las preguntas al usuario,
    calculo el porcentaje de cumplimiento y genero las recomendaciones necesarias.
    """
    # Muestro un encabezado visual para separar cada KPA
    print("\n" + "="*60)
    print(f"Evaluando KPA: {nombre_kpa}")
    print("="*60)
    
    # Inicializo tres listas para almacenar diferentes aspectos de las respuestas
    respuestas_val = []  # Aquí guardo solo los valores numéricos para calcular el porcentaje
    respuestas_raw = []  # En esta lista guardo la información completa de cada respuesta
    detalles = []  # Aquí almaceno un resumen legible para el informe final
    
    # Recorro todas las preguntas de esta KPA
    for p in preguntas:
        # Pido al usuario que responda la pregunta y obtengo su valor y opción
        val, opcion = respuesta_usuario(p)
        
        # Guardo el valor numérico para el cálculo del porcentaje
        respuestas_val.append(val)
        
        # Almaceno toda la información de la respuesta en formato estructurado
        respuestas_raw.append({
            "pregunta": p,  # La pregunta original
            "opcion": opcion,  # La opción elegida: '1', '2' o '3'
            "valor": val,  # El valor numérico: 1.0, 0.5 o 0.0
            "texto": {"1":"Sí","2":"Parcial","3":"No"}[opcion]  # Convierto la opción a texto legible
        })
        
        # Guardo un resumen detallado para mostrarlo en el informe
        detalles.append({
            "pregunta": p, 
            "respuesta": {
                "opcion": opcion, 
                "texto": {"1":"Sí","2":"Parcial","3":"No"}[opcion], 
                "valor": val
            }
        })
    
    # Calculo el porcentaje de cumplimiento de esta KPA
    # Sumo todos los valores y divido entre el número total de respuestas, luego multiplico por 100
    porcentaje = (sum(respuestas_val) / len(respuestas_val)) * 100
    
    # Clasifico el estado según el porcentaje obtenido (Implementada, Parcial, Deficiente)
    estado = estado_porcentaje(porcentaje)
    
    # Genero recomendaciones personalizadas basándome en las respuestas del usuario
    recomendaciones = generar_recomendaciones_por_respuestas(nombre_kpa, respuestas_raw)
    
    # Devuelvo un diccionario con toda la información de la evaluación de esta KPA
    return {
        "kpa": nombre_kpa,  # Nombre de la KPA evaluada
        "porcentaje": round(porcentaje, 2),  # Porcentaje redondeado a 2 decimales
        "estado": estado,  # Clasificación: Implementada, Parcial o Deficiente
        "detalles": detalles,  # Detalles de cada pregunta y respuesta
        "recomendaciones": recomendaciones,  # Lista de recomendaciones personalizadas
        "respuestas_raw": respuestas_raw  # Datos completos de las respuestas
    }

def generar_recomendaciones_por_respuestas(kpa, respuestas_raw):
    """
    Esta función genera recomendaciones inteligentes según las respuestas del usuario.
    Si hay problemas (respuestas "Parcial" o "No"), añado recomendaciones genéricas
    de RECOMENDACIONES_BASE y también recomendaciones específicas para cada pregunta fallida.
    """
    lista = []  # Inicializo la lista donde guardaré todas las recomendaciones
    
    # Filtro las respuestas problemáticas (solo las que son "Parcial" o "No")
    problemas = [r for r in respuestas_raw if r['opcion'] in ('2','3')]
    
    if problemas:  # Si hay problemas detectados
        # Primero añado las recomendaciones genéricas de esta KPA desde RECOMENDACIONES_BASE
        lista.extend(RECOMENDACIONES_BASE.get(kpa, []))
        
        # Ahora genero recomendaciones específicas para cada pregunta fallida
        for r in problemas:
            texto_preg = r['pregunta']  # Obtengo el texto de la pregunta
            
            if r['opcion'] == '3':  # Si la respuesta fue "No"
                # Indico que es un problema grave que debe priorizarse
                lista.append(f"Problema detectado: '{texto_preg}' -> No implementado. Revisar y priorizar su corrección.")
            elif r['opcion'] == '2':  # Si la respuesta fue "Parcial"
                # Sugiero mejorar la formalidad de esta práctica
                lista.append(f"Problema parcial: '{texto_preg}' -> Mejorar formalidad y consistencia.")
    else:
        # Si todas las respuestas fueron "Sí", felicito y sugiero mantener el nivel
        lista.append("Todas las prácticas clave parecen estar satisfechas. Mantener procesos y evidencias.")
    
    # Elimino recomendaciones duplicadas pero mantengo el orden original
    visto = set()  # Set para trackear qué recomendaciones ya he visto
    salida = []  # Lista final sin duplicados
    for contenido in lista:
        if contenido not in visto:  # Si no la he visto antes
            salida.append(contenido)  # La añado a la salida
            visto.add(contenido)  # Y la marco como vista
    
    return salida

def evaluar_todas_las_kpas():
    """
    Esta función ejecuta la evaluación completa de todas las KPAs del proyecto.
    Recorro cada KPA, hago todas sus preguntas y almaceno los resultados.
    """
    resultados = []  # Lista donde guardaré los resultados de todas las KPAs
    
    # Recorro el diccionario KPAS que contiene todas las áreas clave de proceso
    for kpa, preguntas in KPAS.items():
        # Evalúo cada KPA y obtengo su resultado completo
        respuestas = evaluar_kpa(kpa, preguntas)
        # Añado el resultado a mi lista
        resultados.append(respuestas)
    
    return resultados  # Devuelvo la lista con todas las evaluaciones

def diagnostico_general(resultados):
    """
    Esta función calcula el diagnóstico general del proyecto basándose en todas las KPAs.
    Cuento cuántas están implementadas, parciales o deficientes y determino si cumple Nivel 2.
    """
    # Inicializo un diccionario con contadores para cada categoría
    resumen = {
        "implementadas": 0,  # Contador de KPAs bien implementadas (≥80%)
        "parciales": 0,  # Contador de KPAs parcialmente implementadas (50-79%)
        "deficientes": 0,  # Contador de KPAs deficientes (<50%)
        "por_kpa": {}  # Diccionario para guardar el porcentaje de cada KPA
    }
    
    # Analizo cada resultado individual
    for r in resultados:
        # Guardo el porcentaje de esta KPA en el resumen
        resumen["por_kpa"][r["kpa"]] = r["porcentaje"]
        
        # Incremento el contador correspondiente según el estado de la KPA
        if r["estado"] == "Implementada":
            resumen["implementadas"] += 1  # Incremento si está bien implementada
        elif r["estado"] == "Parcialmente implementada":
            resumen["parciales"] += 1  # Incremento si está parcial
        else:
            resumen["deficientes"] += 1  # Incremento si está deficiente
    
    # Determino si el proyecto cumple el Nivel 2 de CMMI
    # Solo cumple si TODAS las KPAs están en estado "Implementada"
    cumple_nivel2 = (resumen["implementadas"] == len(KPAS))
    
    return resumen, cumple_nivel2  # Devuelvo el resumen y el veredicto final

def recomendaciones_para_alcanzar_nivel2(resultados):
    """
    Esta función genera un listado de recomendaciones para alcanzar el Nivel 2.
    Solo incluyo las KPAs que no están completamente implementadas.
    """
    recomendaciones = []  # Lista para almacenar las recomendaciones
    
    # Recorro todos los resultados buscando KPAs problemáticas
    for r in resultados:
        if r["estado"] != "Implementada":  # Si no está completamente implementada
            # Añado esta KPA con su estado y recomendaciones
            recomendaciones.append({
                "kpa": r["kpa"],
                "estado": r["estado"],
                "recomendaciones": r["recomendaciones"]
            })
    
    # Si no hay recomendaciones, significa que todo está bien
    if not recomendaciones:
        return ["El proyecto cumple los requisitos de Nivel 2. Mantener las prácticas actuales."]
    
    return recomendaciones

def conclusion_final(cumple_nivel2, summary):
    """
    Genero la conclusión final del diagnóstico con fecha y hora.
    Determino si el proyecto cumple o no el Nivel 2 de CMMI.
    """
    # Obtengo la fecha y hora actual en formato legible
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if cumple_nivel2:  # Si cumple todos los requisitos
        mensaje = f"Conclusión ({ahora}): El proyecto cumple el Nivel 2 de CMMI."
    else:  # Si no cumple
        mensaje = f"Conclusión ({ahora}): El proyecto NO cumple el Nivel 2 de CMMI. Recomendado trabajar las áreas deficientes y parciales."
    
    return mensaje

def menu_principal():
    """
    Muestro el menú principal de mi herramienta con las opciones disponibles.
    El usuario puede evaluar todas las KPAs, una específica, o salir.
    """
    # Imprimo un encabezado visual llamativo
    print("\n" + "#"*60)
    print("HERRAMIENTA DIAGNÓSTICO CMMI NIVEL 2")
    print("#"*60)
    
    # Listo las opciones disponibles
    print("Opciones:")
    print("  1) Evaluar todas las KPAs (recomendado)")  # Opción para evaluación completa
    print("  2) Evaluar una KPA específica")  # Opción para evaluación individual
    print("  3) Salir")  # Opción para terminar el programa
    
    # Leo la opción del usuario
    opcion = input("Elige una opción (1/2/3): ").strip()
    
    return opcion  # Devuelvo la opción elegida

def elegir_kpa():
    """
    Esta función permite al usuario seleccionar una KPA específica del listado.
    Muestro todas las KPAs numeradas y valido la selección.
    """
    print("\nSelecciona la KPA a evaluar:")
    
    # Obtengo la lista de todas las KPAs disponibles
    kpas = list(KPAS.keys())
    
    # Muestro cada KPA con su número
    i = 1
    for k in kpas:
        print(f"  {i}) {k}")
        i += 1
    
    # Pido al usuario que elija un número
    opcion = input(f"Elige (1-{len(kpas)}): ").strip()
    
    # Valido que la opción sea un número y esté en el rango correcto
    if opcion.isdigit() and 1 <= int(opcion) <= len(kpas):
        # Devuelvo la KPA seleccionada (resto 1 porque las listas empiezan en 0)
        return kpas[int(opcion) - 1]
    else:
        # Si la opción no es válida, muestro error y vuelvo a preguntar recursivamente
        print("Opción no válida.")
        return elegir_kpa()
    
def main():
    """
    Esta es la función principal que ejecuta todo el programa.
    Controlo el flujo de la aplicación, manejo el menú y coordino las evaluaciones.
    """
    # Mensaje de bienvenida
    print("Bienvenido a la herramienta de diagnóstico CMMI Nivel 2.")
    
    # Pido el nombre del proyecto al usuario
    nombre_proyecto = input("Nombre del proyecto: ").strip()
    
    # Si no ingresa nombre, asigno uno por defecto
    if nombre_proyecto == "":
        nombre_proyecto = "Proyecto_sin_nombre"

    # Bucle principal del programa - se ejecuta hasta que el usuario decida salir
    while True:
        # Muestro el menú y obtengo la opción seleccionada
        opcion = menu_principal()
        
        # Opción 1: Evaluar todas las KPAs (evaluación completa)
        if opcion == "1":
            # Ejecuto la evaluación completa de todas las KPAs
            resultados = evaluar_todas_las_kpas()
            
            # Calculo el diagnóstico general y verifico si cumple Nivel 2
            resumen, cumple_nivel2 = diagnostico_general(resultados)

            # Muestro el encabezado del informe completo
            print("\n" + "="*80)
            print("INFORME RESUMIDO (todas las KPAs):")
            print("="*80)

            # Recorro y muestro los resultados de cada KPA evaluada
            for r in resultados:
                # Imprimo la información de cada KPA
                print(f"\nKPA: {r['kpa']}")
                print(f"  - Cumplimiento: {r['porcentaje']}%")
                print(f"  - Estado: {r['estado']}")
                
                # Muestro las respuestas dadas a cada pregunta
                print("  - Respuestas:")
                for d in r["detalles"]:
                    print(f"     * {d['pregunta']} -> {d['respuesta']['texto']}")
                
                # Listo las recomendaciones generadas para esta KPA
                print("  - Recomendaciones:")
                for rec in r["recomendaciones"]:
                    print(f"     - {rec}")

            # Ahora muestro el resumen general consolidado
            print("\n" + "="*80)
            print("Resumen general:")
            print(f"  KPAs implementadas: {resumen['implementadas']}")
            print(f"  KPAs parcialmente implementadas: {resumen['parciales']}")
            print(f"  KPAs deficientes: {resumen['deficientes']}")

            # Muestro si cumple o no el Nivel 2 de CMMI
            print(f"\nVerificación nivel 2: {'Cumple' if cumple_nivel2 else 'No cumple'}")
            print(conclusion_final(cumple_nivel2, resumen))

            # Pregunto si quiere hacer otra evaluación
            repetir = input("\n¿Quieres realizar otra evaluación? (s/n): ").strip().lower()
            if repetir != "s":
                print("Fin. ¡Buena suerte con la práctica!")
                break  # Salgo del bucle principal

        # Opción 2: Evaluar una KPA específica
        elif opcion == "2":
            # Permito al usuario seleccionar qué KPA quiere evaluar
            kpa = elegir_kpa()
            
            # Evalúo solo esa KPA seleccionada
            respuesta = evaluar_kpa(kpa, KPAS[kpa])

            # Muestro el informe de esta KPA individual
            print("\n" + "="*60)
            print(f"Informe KPA seleccionada: {kpa}")
            print("="*60)
            print(f"Cumplimiento: {respuesta['porcentaje']}%")
            print(f"Estado: {respuesta['estado']}")
            
            # Listo las respuestas
            print("\nRespuestas:")
            for d in respuesta["detalles"]:
                print(f" - {d['pregunta']} -> {d['respuesta']['texto']}")
            
            # Listo las recomendaciones
            print("\nRecomendaciones:")
            for rec in respuesta["recomendaciones"]:
                print(f" - {rec}")

            # Pregunto qué quiere hacer a continuación
            while True:
                repetir = input("\n¿Quieres evaluar otra KPA o volver al menú principal? (v=volver, s=salir): ").strip().lower()
                if repetir in ("v", "s"):
                    break  # Salgo del bucle de validación
                else:
                    print("Opción inválida. Solo puedes introducir 'v' o 's'.")

            # Si eligió salir, termino el programa
            if repetir == "s":
                print("Fin. ¡Buena suerte con la práctica!")
                break

        # Opción 3: Salir del programa
        elif opcion == "3":
            print("Saliendo. ¡Hasta luego!")
            break  # Salgo del bucle principal
        
        # Si ingresa una opción inválida
        else:
            print("Opción no válida. Intenta de nuevo.")

# Este bloque solo se ejecuta si ejecuto este archivo directamente (no si lo importo)
if __name__ == "__main__":
    main()  # Inicio la ejecución del programa
