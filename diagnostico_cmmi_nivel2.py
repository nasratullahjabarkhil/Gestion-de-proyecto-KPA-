import json
import datetime
from KPAS import KPAS
from VALOR_RESPUESTA import VALOR_RESPUESTA
from RECOMENDACIONES_BASE import RECOMENDACIONES_BASE
from porcentaje import estado_porcentaje


def respuesta_usuario(pregunta):
    """Pedimos respuesta al usuario para una pregunta con estas opciones Sí/Parcial/No."""
    while True:
        print("\n" + pregunta)
        print("  1) Sí")
        print("  2) Parcial")
        print("  3) No")
        opcion = input("Elige una opción (1/2/3): ").strip()
        if opcion in VALOR_RESPUESTA: # cogemos el vlaor de la respuesta de VALOR_RESPUESTA
            return VALOR_RESPUESTA[opcion], opcion
        print("Opción no válida. Intenta de nuevo.") # si la opcion no es en las opciones da que no es valida

def evaluar_kpa(nombre_kpa, preguntas): # recibe nombre de kpa y sus correspondientes preguntas
    """Realizamos la evaluación para una KPA. Devolvemos respuestas y metadatos."""
    print("\n" + "="*60)
    print(f"Evaluando KPA: {nombre_kpa}")
    print("="*60) # imprimimos 60 =
    respuestas_val = [] # creamos lista de valor de respuestas 
    respuestas_raw = [] # # creamos una lista de respuestas con mas detalles
    detalles = []  # guardamos un resumen legible de cada respuesta en esta lista 
    for p in preguntas:
        # aqui segun la respuesta del usaurio cogemos su valor 
        val, opcion = respuesta_usuario(p)
        respuestas_val.append(val)
        respuestas_raw.append({
            "pregunta": p,
            "opcion": opcion, # '1','2','3'
            "valor": val, # valor de la respuesta (Si, Parcial, No)
            "texto": {"1":"Sí","2":"Parcial","3":"No"}[opcion]
        })
        detalles.append({"pregunta": p, "respuesta": {"opcion": opcion, "texto": {"1":"Sí","2":"Parcial","3":"No"}[opcion], "valor": val}})
    # Calculamos porcentaje
    # dividimos la suma de los valores de respuesta entre el numero de respuestas  
    porcentaje = (sum(respuestas_val) / len(respuestas_val)) * 100
    estado = estado_porcentaje(porcentaje) # verificamos el estado segun el resutlado 
    
    # recomendaciones si hay respuestas parcial o no, las incluimos de recomendaciones base 
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
    generamos una recomendacion segun las respuestas si hay parcial o no 
    """
    lista = []
    # añadimos recomendaciones si hay problemas (parcial, no)
    problemas = [r for r in respuestas_raw if r['opcion'] in ('2','3')]
    if problemas:
        lista.extend(RECOMENDACIONES_BASE.get(kpa, []))
        # Añadir recomendadion concreta para la pregunta fallida 
        for r in problemas:
            texto_preg = r['pregunta']
            if r['opcion'] == '3':
                lista.append(f"Problema detectado: '{texto_preg}' -> No implementado. Revisar y priorizar su corrección.")
            elif r['opcion'] == '2':
                lista.append(f"Problema parcial: '{texto_preg}' -> Mejorar formalidad y consistencia.")
    else:
        lista.append("Todas las prácticas clave parecen estar satisfechas. Mantener procesos y evidencias.")
    # Evitamos las duplicaciones manteniendo orden 
    visto = set()
    salida = []
    for contenido in lista:
        if contenido not in visto:
            salida.append(contenido)
            visto.add(contenido)
    return salida

def evaluar_todas_las_kpas():
    """Evalúamos todas las kpas y devolvemos una lisa"""
    resultados = []
    for kpa, preguntas in KPAS.items():
        respuestas = evaluar_kpa(kpa, preguntas)
        resultados.append(respuestas)
    return resultados

def diagnostico_general(resultados):
    """Aqui calculamos el diagnostico a partir de la lista de resultados."""
    resumen = {
        "implementadas": 0,
        "parciales": 0,
        "deficientes": 0,
        "por_kpa": {}
    }
    for r in resultados:
        resumen["por_kpa"][r["kpa"]] = r["porcentaje"]
        if r["estado"] == "Implementada":
            resumen["implementadas"] += 1
        elif r["estado"] == "Parcialmente implementada":
            resumen["parciales"] += 1
        else:
            resumen["deficientes"] += 1
    # Verificamos el nivel 2
    cumple_nivel2 = (resumen["implementadas"] == len(KPAS))
    return resumen, cumple_nivel2

def recomendaciones_para_alcanzar_nivel2(resultados):
    """
    Generamos recomendaciones generales para alcanzar el Nivel 2
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
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if cumple_nivel2:
        mensaje = f"Conclusión ({ahora}): El proyecto cumple el Nivel 2 de CMMI."
    else:
        mensaje = f"Conclusión ({ahora}): El proyecto NO cumple el Nivel 2 de CMMI. Recomendado trabajar las áreas deficientes y parciales."
    return mensaje

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


def elegir_kpa():
    print("\nSelecciona la KPA a evaluar:")
    kpas = list(KPAS.keys())
    
    i = 1
    for k in kpas:
        print(f"  {i}) {k}")
        i += 1

    opcion = input(f"Elige (1-{len(kpas)}): ").strip()

    if opcion.isdigit() and 1 <= int(opcion) <= len(kpas):
        return kpas[int(opcion) - 1]
    else:
        print("Opción no válida.")
        return elegir_kpa()
    
def main():
    print("Bienvenido a la herramienta de diagnóstico CMMI Nivel 2.")
    nombre_proyecto = input("Nombre del proyecto: ").strip()
    if nombre_proyecto == "":
        nombre_proyecto = "Proyecto_sin_nombre"

    while True:
        opcion = menu_principal()
        if opcion == "1":
            resultados = evaluar_todas_las_kpas()
            resumen, cumple_nivel2 = diagnostico_general(resultados)

            print("\n" + "="*80)
            print("INFORME RESUMIDO (todas las KPAs):")
            print("="*80)

            # Mostramos resultados de cada KPA
            for r in resultados:
                print(f"\nKPA: {r['kpa']}")
                print(f"  - Cumplimiento: {r['porcentaje']}%")
                print(f"  - Estado: {r['estado']}")
                print("  - Respuestas:")
                for d in r["detalles"]:
                    print(f"     * {d['pregunta']} -> {d['respuesta']['texto']}")
                print("  - Recomendaciones:")
                for rec in r["recomendaciones"]:
                    print(f"     - {rec}")

            #  el resumen general
            print("\n" + "="*80)
            print("Resumen general:")
            print(f"  KPAs implementadas: {resumen['implementadas']}")
            print(f"  KPAs parcialmente implementadas: {resumen['parciales']}")
            print(f"  KPAs deficientes: {resumen['deficientes']}")

            print(f"\nVerificación nivel 2: {'Cumple' if cumple_nivel2 else 'No cumple'}")
            print(conclusion_final(cumple_nivel2, resumen))

            # Preguntamos si quiere repetir
            repetir = input("\n¿Quieres realizar otra evaluación? (s/n): ").strip().lower()
            if repetir != "s":
                print("Fin. ¡Buena suerte con la práctica!")
                break


        elif opcion == "2":
            kpa = elegir_kpa()
            respuesta = evaluar_kpa(kpa, KPAS[kpa])

            print("\n" + "="*60)
            print(f"Informe KPA seleccionada: {kpa}")
            print("="*60)
            print(f"Cumplimiento: {respuesta['porcentaje']}%")
            print(f"Estado: {respuesta['estado']}")
            print("\nRespuestas:")
            for d in respuesta["detalles"]:
                print(f" - {d['pregunta']} -> {d['respuesta']['texto']}")
            print("\nRecomendaciones:")
            for rec in respuesta["recomendaciones"]:
                print(f" - {rec}")

            while True:
                repetir = input("\n¿Quieres evaluar otra KPA o volver al menú principal? (v=volver, s=salir): ").strip().lower()
                if repetir in ("v", "s"):
                    break
                else:
                    print("Opción inválida. Solo puedes introducir 'v' o 's'.")

            if repetir == "s":
                print("Fin. ¡Buena suerte con la práctica!")
                break

        elif opcion == "3":
            print("Saliendo. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
