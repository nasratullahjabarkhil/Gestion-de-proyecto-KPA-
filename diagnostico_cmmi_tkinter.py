# diagnostico_cmmi_tkinter.py
# Este archivo implementa la interfaz gráfica de mi herramienta de diagnóstico CMMI
# Utilizo Tkinter para crear una aplicación con ventanas, botones y formularios

import tkinter as tk  # Importo Tkinter para crear la interfaz gráfica
from tkinter import ttk, messagebox  # Importo widgets mejorados y cuadros de diálogo
from KPAS import KPAS  # Cargo las 5 KPAs con sus preguntas
from VALOR_RESPUESTA import VALOR_RESPUESTA  # Valores numéricos de las respuestas
from RECOMENDACIONES_BASE import RECOMENDACIONES_BASE  # Recomendaciones base para cada KPA
from porcentaje import estado_porcentaje  # Función para clasificar el estado según porcentaje
import datetime  # Para registrar fecha y hora en la conclusión


# --- LÓGICA (adaptada de la versión CLI) ---

def generar_recomendaciones_por_respuestas(kpa, respuestas_raw):
    """
    Esta función genera recomendaciones personalizadas según las respuestas del usuario.
    Es la misma lógica que en la versión CLI, pero adaptada para la GUI.
    """
    lista = []  # Lista donde guardaré todas las recomendaciones
    
    # Filtro solo las respuestas problemáticas (Parcial o No)
    problemas = [r for r in respuestas_raw if r['opcion'] in ('2', '3')]
    
    if problemas:  # Si hay problemas detectados
        # Añado las recomendaciones genéricas de esta KPA
        lista.extend(RECOMENDACIONES_BASE.get(kpa, []))
        
        # Genero recomendaciones específicas para cada pregunta con problemas
        for r in problemas:
            texto_preg = r['pregunta']
            if r['opcion'] == '3':  # Si respondió "No"
                lista.append(f"'{texto_preg}' → No implementado. Priorizar su corrección.")
            elif r['opcion'] == '2':  # Si respondió "Parcial"
                lista.append(f"'{texto_preg}' → Parcialmente implementado. Mejorar formalidad.")
    else:
        # Si todo está bien, felicito al usuario
        lista.append("Todas las prácticas clave parecen estar satisfechas. Mantener procesos y evidencias.")
    
    # Elimino duplicados manteniendo el orden
    visto = set()
    salida = []
    for contenido in lista:
        if contenido not in visto:
            salida.append(contenido)
            visto.add(contenido)
    
    return salida


def evaluar_kpa(nombre_kpa, respuestas_usuario):
    """
    Evalúo una KPA completa recibiendo las respuestas del usuario desde la GUI.
    La diferencia con la versión CLI es que aquí recibo las respuestas como parámetro
    en lugar de pedirlas interactivamente.
    """
    # Obtengo las preguntas de esta KPA
    preguntas = KPAS[nombre_kpa]
    respuestas_raw = []  # Lista para almacenar información detallada de cada respuesta
    valores = []  # Lista solo con los valores numéricos para calcular el porcentaje

    # Proceso cada pregunta con su respuesta correspondiente
    for p, opcion in zip(preguntas, respuestas_usuario):
        # Obtengo el valor numérico de la respuesta desde VALOR_RESPUESTA
        val = VALOR_RESPUESTA[opcion]
        
        # Guardo toda la información de esta respuesta
        respuestas_raw.append({
            "pregunta": p,  # Texto de la pregunta
            "opcion": opcion,  # Opción seleccionada: '1', '2' o '3'
            "valor": val,  # Valor numérico: 1.0, 0.5 o 0.0
            "texto": {"1": "Sí", "2": "Parcial", "3": "No"}[opcion]  # Texto legible
        })
        
        # Añado el valor a la lista para el cálculo del porcentaje
        valores.append(val)

    # Calculo el porcentaje de cumplimiento (o 0 si no hay valores)
    porcentaje = (sum(valores) / len(valores)) * 100 if valores else 0
    
    # Clasifico el estado según el porcentaje obtenido
    estado = estado_porcentaje(porcentaje)
    
    # Genero recomendaciones personalizadas
    recomendaciones = generar_recomendaciones_por_respuestas(nombre_kpa, respuestas_raw)

    # Devuelvo un diccionario con toda la información de la evaluación
    return {
        "kpa": nombre_kpa,
        "porcentaje": round(porcentaje, 2),  # Redondeo a 2 decimales
        "estado": estado,
        "respuestas": respuestas_raw,
        "recomendaciones": recomendaciones
    }


def generar_resumen_general(resultados):
    """
    Genero un resumen consolidado de todas las KPAs evaluadas.
    Cuento cuántas están implementadas, parciales o deficientes.
    """
    resumen = {
        "implementadas": 0,  # Contador de KPAs bien implementadas
        "parciales": 0,  # Contador de KPAs parcialmente implementadas
        "deficientes": 0,  # Contador de KPAs deficientes
        "por_kpa": {}  # Diccionario con el porcentaje de cada KPA
    }
    
    # Analizo cada resultado
    for r in resultados:
        # Guardo el porcentaje de esta KPA
        resumen["por_kpa"][r["kpa"]] = r["porcentaje"]
        
        # Incremento el contador correspondiente según su estado
        if r["estado"] == "Implementada":
            resumen["implementadas"] += 1
        elif r["estado"] == "Parcialmente implementada":
            resumen["parciales"] += 1
        else:
            resumen["deficientes"] += 1
    
    # El proyecto cumple Nivel 2 solo si TODAS las KPAs están implementadas
    cumple_nivel2 = (resumen["implementadas"] == len(KPAS))
    
    return resumen, cumple_nivel2


def conclusion_final(cumple_nivel2):
    """
    Genero la conclusión final con fecha y hora actual.
    """
    # Obtengo la fecha y hora en formato legible
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if cumple_nivel2:  # Si cumple todos los requisitos
        mensaje = f"Conclusión ({ahora}): El proyecto cumple el Nivel 2 de CMMI."
    else:  # Si no cumple
        mensaje = f"Conclusión ({ahora}): El proyecto NO cumple el Nivel 2 de CMMI. Recomendado trabajar las áreas deficientes y parciales."
    
    return mensaje


# --- INTERFAZ TKINTER ---

class CMMIApp:
    """
    Esta es mi clase principal que gestiona toda la interfaz gráfica.
    Controlo las diferentes pantallas, formularios y la navegación entre ellas.
    """
    
    def __init__(self, root):
        """
        Constructor de la aplicación. Aquí inicializo la ventana principal
        y todas las variables que necesitaré durante la ejecución.
        """
        # Guardo la referencia a la ventana principal
        self.root = root
        
        # Configuro el título de la ventana
        self.root.title("Diagnóstico CMMI Nivel 2")
        
        # Establezco el tamaño de la ventana (ancho x alto)
        self.root.geometry("920x700")

        # Creo una variable para almacenar el nombre del proyecto
        self.nombre_proyecto = tk.StringVar()
        
        # Variable para saber qué KPA estoy evaluando actualmente
        self.kpa_actual = None

        # Variables para la evaluación por lotes (cuando evalúo todas las KPAs)
        self.batch_kpas = []  # Lista de KPAs a evaluar
        self.batch_index = 0  # Índice de la KPA actual en el proceso batch
        self.batch_results = []  # Resultados acumulados de las evaluaciones

        # Muestro la pantalla inicial
        self.frame_inicio()

    def limpiar_frame(self):
        """
        Esta función elimina todos los widgets de la ventana.
        La uso antes de mostrar una nueva pantalla para limpiar la anterior.
        """
        # Recorro todos los widgets hijos de la ventana principal y los destruyo
        for widget in self.root.winfo_children():
            widget.destroy()

    def frame_inicio(self):
        """
        Muestro la pantalla de inicio con el menú principal.
        Aquí el usuario puede elegir entre evaluar todas las KPAs, una específica, o salir.
        """
        # Limpio cualquier contenido previo de la ventana
        self.limpiar_frame()
        
        # Creo y muestro el título principal
        tk.Label(self.root, text="Herramienta Diagnóstico CMMI Nivel 2",
                 font=("Helvetica", 18, "bold")).pack(pady=20)
        
        # Etiqueta para el campo de nombre del proyecto
        tk.Label(self.root, text="Nombre del proyecto:").pack()
        
        # Campo de entrada para que el usuario escriba el nombre del proyecto
        tk.Entry(self.root, textvariable=self.nombre_proyecto, width=60).pack(pady=5)
        
        # Botón para evaluar todas las KPAs
        ttk.Button(self.root, text="Evaluar todas las KPAs", command=self.evaluar_todas).pack(pady=10)
        
        # Botón para evaluar una KPA específica
        ttk.Button(self.root, text="Evaluar una KPA específica", command=self.menu_kpa).pack(pady=10)
        
        # Botón para salir de la aplicación
        ttk.Button(self.root, text="Salir", command=self.root.quit).pack(pady=10)

    def menu_kpa(self):
        """
        Muestro un menú con todas las KPAs disponibles para que el usuario elija una.
        Utilizo un canvas con scrollbar para que pueda desplazarse si hay muchas KPAs.
        """
        # Limpio la ventana
        self.limpiar_frame()
        
        # Título de la pantalla
        tk.Label(self.root, text="Selecciona una KPA:", font=("Helvetica", 14, "bold")).pack(pady=20)
        
        # Creo un canvas (lienzo) que me permite añadir scrollbar
        canvas = tk.Canvas(self.root)
        
        # Creo una barra de desplazamiento vertical
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        
        # Frame que contendrá todos los botones de las KPAs
        scroll_frame = ttk.Frame(canvas)

        # Configuro el evento para actualizar la región de scroll cuando cambie el tamaño
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")  # Actualizo la región scrollable
            )
        )

        # Creo una ventana dentro del canvas para contener el frame
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        
        # Conecto el canvas con la scrollbar
        canvas.configure(yscrollcommand=scrollbar.set, height=420)

        # Creo un botón para cada KPA disponible
        for kpa in KPAS.keys():
            # Cada botón llama a formulario_kpa con la KPA correspondiente
            # Uso lambda con parámetro por defecto para capturar el valor correcto de kpa
            ttk.Button(scroll_frame, text=kpa, width=80,
                       command=lambda k=kpa: self.formulario_kpa(k)).pack(pady=5)

        # Posiciono el canvas y la scrollbar en la ventana
        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y")
        
        # Botón para volver al menú principal
        ttk.Button(self.root, text="Volver", command=self.frame_inicio).pack(pady=10)

    # --- Evaluar una sola KPA ---
    
    def formulario_kpa(self, kpa):
        """
        Muestro el formulario con todas las preguntas de una KPA específica.
        Para cada pregunta, creo botones de opción (radio buttons) con las opciones Sí/Parcial/No.
        """
        # Limpio la ventana
        self.limpiar_frame()
        
        # Guardo qué KPA estoy evaluando
        self.kpa_actual = kpa
        
        # Muestro el nombre de la KPA como título
        tk.Label(self.root, text=f"KPA: {kpa}", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Obtengo las preguntas de esta KPA
        preguntas = KPAS[kpa]

        # Lista para almacenar las variables de cada pregunta
        self.vars = []
        
        # Creo un frame para contener las preguntas con scroll
        frame_preguntas = ttk.Frame(self.root)
        frame_preguntas.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas para permitir scroll
        canvas = tk.Canvas(frame_preguntas)
        scrollbar = ttk.Scrollbar(frame_preguntas, orient="vertical", command=canvas.yview)
        preguntas_frame = ttk.Frame(canvas)

        # Configuro el scroll region
        preguntas_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=preguntas_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, height=420)

        # Creo los elementos para cada pregunta
        for i, p in enumerate(preguntas):
            # Frame individual para cada pregunta
            frame_p = ttk.Frame(preguntas_frame)
            frame_p.pack(anchor="w", pady=6, fill="x")
            
            # Etiqueta con el texto de la pregunta
            lbl = tk.Label(frame_p, text=f"{i+1}. {p}", wraplength=760, justify="left")
            lbl.pack(anchor="w")
            
            # Variable para almacenar la respuesta de esta pregunta
            var = tk.StringVar()
            self.vars.append(var)
            
            # Defino las tres opciones de respuesta
            opciones = [("Sí", "1"), ("Parcial", "2"), ("No", "3")]
            
            # Frame para los radio buttons
            opt_frame = ttk.Frame(frame_p)
            opt_frame.pack(anchor="w", pady=2)
            
            # Creo un radio button para cada opción
            for txt, val in opciones:
                ttk.Radiobutton(opt_frame, text=txt, variable=var, value=val).pack(side="left", padx=5)

        # Posiciono el canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame para los botones de acción
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Botón para evaluar (procesar las respuestas)
        ttk.Button(btn_frame, text="Evaluar", command=self.mostrar_resultado_kpa).pack(side="left", padx=5)
        
        # Botón para volver al menú de KPAs
        ttk.Button(btn_frame, text="Volver", command=self.menu_kpa).pack(side="left")

    def mostrar_resultado_kpa(self):
        """
        Proceso las respuestas del formulario, evalúo la KPA y muestro los resultados.
        Primero valido que todas las preguntas estén respondidas.
        """
        # Recopilo todas las respuestas seleccionadas por el usuario
        respuestas_usuario = [v.get() for v in self.vars]
        
        # Verifico que no haya preguntas sin responder (valores vacíos)
        if "" in respuestas_usuario:
            # Muestro un mensaje de error si falta alguna respuesta
            messagebox.showerror("Error", "Responde todas las preguntas antes de continuar.")
            return
        
        # Evalúo la KPA con las respuestas del usuario
        resultado = evaluar_kpa(self.kpa_actual, respuestas_usuario)
        
        # Muestro el informe de resultados
        self.mostrar_informe(resultado, volver_menu=True)

    def mostrar_informe(self, resultado, volver_menu=False):
        """
        Muestro el informe detallado de una KPA evaluada.
        Incluyo porcentaje, estado, respuestas y recomendaciones.
        """
        # Limpio la ventana
        self.limpiar_frame()
        
        # Título con el nombre de la KPA
        tk.Label(self.root, text=f"Informe de {resultado['kpa']}",
                 font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Muestro el porcentaje de cumplimiento
        tk.Label(self.root, text=f"Cumplimiento: {resultado['porcentaje']}%").pack()
        
        # Muestro el estado (Implementada, Parcial, Deficiente)
        tk.Label(self.root, text=f"Estado: {resultado['estado']}").pack(pady=5)

        # Creo un frame con un área de texto scrollable para mostrar detalles
        frame_texto = ttk.Frame(self.root)
        frame_texto.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Widget de texto para mostrar la información detallada
        text = tk.Text(frame_texto, wrap="word")
        text.pack(fill="both", expand=True, side="left")
        
        # Scrollbar para el área de texto
        scroll = ttk.Scrollbar(frame_texto, command=text.yview, orient="vertical")
        scroll.pack(side="right", fill="y")
        text.configure(yscrollcommand=scroll.set)

        # Inserto el contenido en el área de texto
        text.insert("end", "Respuestas:\n\n")
        
        # Muestro cada pregunta con su respuesta
        for r in resultado["respuestas"]:
            text.insert("end", f" - {r['pregunta']}\n     → {r['texto']}\n")
        
        text.insert("end", "\nRecomendaciones:\n\n")
        
        # Muestro todas las recomendaciones
        for rec in resultado["recomendaciones"]:
            text.insert("end", f" - {rec}\n")

        # Frame para el botón de volver
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Botón para regresar al menú principal
        if volver_menu:
            ttk.Button(btn_frame, text="Volver al menú", command=self.frame_inicio).pack()
        else:
            ttk.Button(btn_frame, text="Volver al menú", command=self.frame_inicio).pack()

    # --- Evaluar todas las KPAs (batch/lote) ---
    
    def evaluar_todas(self):
        """
        Inicio el proceso de evaluación de todas las KPAs de forma secuencial.
        El usuario responderá las preguntas de cada KPA una por una.
        """
        # Obtengo la lista de todas las KPAs a evaluar
        self.batch_kpas = list(KPAS.keys())
        
        # Reseteo el índice a 0 (empiezo por la primera KPA)
        self.batch_index = 0
        
        # Limpio la lista de resultados previos
        self.batch_results = []
        
        # Verifico que haya KPAs para evaluar
        if not self.batch_kpas:
            messagebox.showinfo("Info", "No hay KPAs definidas.")
            return
        
        # Pido confirmación al usuario antes de comenzar
        if messagebox.askyesno("Confirmar", "Se van a evaluar todas las KPAs de forma secuencial. ¿Continuar?"):
            # Si confirma, muestro el formulario de la primera KPA
            self.formulario_kpa_batch(self.batch_index)

    def formulario_kpa_batch(self, index):
        """
        Muestro el formulario de una KPA dentro del proceso de evaluación por lotes.
        Similar a formulario_kpa, pero con un indicador de progreso y botones diferentes.
        """
        # Si ya evalué todas las KPAs, muestro el resumen final
        if index >= len(self.batch_kpas):
            self.mostrar_resumen_general(self.batch_results)
            return

        # Limpio la ventana
        self.limpiar_frame()
        
        # Obtengo la KPA actual
        kpa = self.batch_kpas[index]
        self.kpa_actual = kpa
        
        # Título con indicador de progreso (ej: "KPA [2/5]: Planificación de proyectos")
        tk.Label(self.root, text=f"KPA [{index+1}/{len(self.batch_kpas)}]: {kpa}", 
                 font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Obtengo las preguntas de esta KPA
        preguntas = KPAS[kpa]

        # Lista para almacenar las variables de respuesta
        self.vars = []
        
        # Creo el frame con scroll para las preguntas
        frame_preg = ttk.Frame(self.root)
        frame_preg.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(frame_preg)
        scrollbar = ttk.Scrollbar(frame_preg, orient="vertical", command=canvas.yview)
        preguntas_frame = ttk.Frame(canvas)

        preguntas_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=preguntas_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, height=420)

        # Creo los elementos para cada pregunta (igual que en formulario_kpa)
        for i, p in enumerate(preguntas):
            frame_p = ttk.Frame(preguntas_frame)
            frame_p.pack(anchor="w", pady=6, fill="x")
            lbl = tk.Label(frame_p, text=f"{i+1}. {p}", wraplength=760, justify="left")
            lbl.pack(anchor="w")
            var = tk.StringVar()
            self.vars.append(var)
            opciones = [("Sí", "1"), ("Parcial", "2"), ("No", "3")]
            opt_frame = ttk.Frame(frame_p)
            opt_frame.pack(anchor="w", pady=2)
            for txt, val in opciones:
                ttk.Radiobutton(opt_frame, text=txt, variable=var, value=val).pack(side="left", padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame para los botones
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Botón para guardar las respuestas y continuar con la siguiente KPA
        ttk.Button(btn_frame, text="Guardar y Siguiente", 
                   command=self.guardar_siguiente_batch).pack(side="left", padx=5)
        
        # Botón para cancelar el proceso completo y volver al menú
        ttk.Button(btn_frame, text="Cancelar (volver al menú)", 
                   command=self.cancelar_batch).pack(side="left", padx=5)

    def guardar_siguiente_batch(self):
        """
        Guardo las respuestas de la KPA actual y avanzo a la siguiente.
        Valido que todas las preguntas estén respondidas antes de continuar.
        """
        # Recopilo las respuestas del formulario actual
        respuestas_usuario = [v.get() for v in self.vars]
        
        # Verifico que todas las preguntas estén respondidas
        if "" in respuestas_usuario:
            messagebox.showerror("Error", "Responde todas las preguntas antes de continuar.")
            return
        
        # Evalúo esta KPA con las respuestas del usuario
        resultado = evaluar_kpa(self.kpa_actual, respuestas_usuario)
        
        # Añado el resultado a mi lista acumulada
        self.batch_results.append(resultado)
        
        # Incremento el índice para pasar a la siguiente KPA
        self.batch_index += 1
        
        # Continúo con la siguiente KPA (o muestro el resumen si terminé)
        self.formulario_kpa_batch(self.batch_index)

    def cancelar_batch(self):
        """
        Cancelo el proceso de evaluación por lotes y vuelvo al menú principal.
        Pido confirmación antes de cancelar para evitar pérdida accidental de datos.
        """
        # Pido confirmación al usuario
        if messagebox.askyesno("Confirmar", "Cancelar evaluación de todas las KPAs y volver al menú?"):
            # Si confirma, reseteo todas las variables del proceso batch
            self.batch_kpas = []
            self.batch_index = 0
            self.batch_results = []
            
            # Vuelvo al menú principal
            self.frame_inicio()

    def mostrar_resumen_general(self, resultados):
        """
        Muestro el informe completo con los resultados de todas las KPAs evaluadas.
        Incluyo detalles de cada KPA, resumen general y conclusión sobre el Nivel 2.
        """
        # Limpio la ventana
        self.limpiar_frame()
        
        # Título del informe general
        tk.Label(self.root, text="INFORME RESUMIDO (todas las KPAs)", 
                 font=("Helvetica", 16, "bold")).pack(pady=10)

        # Genero el resumen consolidado y verifico si cumple Nivel 2
        resumen, cumple_nivel2 = generar_resumen_general(resultados)

        # Creo un frame con área de texto scrollable para el informe completo
        frame_texto = ttk.Frame(self.root)
        frame_texto.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Widget de texto para mostrar todo el contenido
        text = tk.Text(frame_texto, wrap="word")
        text.pack(fill="both", expand=True)
        
        # Scrollbar para navegar por el informe
        scroll = ttk.Scrollbar(frame_texto, command=text.yview, orient="vertical")
        scroll.pack(side="right", fill="y")
        text.configure(yscrollcommand=scroll.set)

        # Inserto la información de cada KPA evaluada
        for r in resultados:
            # Nombre de la KPA
            text.insert("end", f"KPA: {r['kpa']}\n")
            
            # Porcentaje de cumplimiento
            text.insert("end", f" - Cumplimiento: {r['porcentaje']}%\n")
            
            # Estado (Implementada, Parcial, Deficiente)
            text.insert("end", f" - Estado: {r['estado']}\n")
            
            # Lista de respuestas dadas
            text.insert("end", " - Respuestas:\n")
            for resp in r['respuestas']:
                text.insert("end", f"    * {resp['pregunta']} → {resp['texto']}\n")
            
            # Recomendaciones para esta KPA
            text.insert("end", " - Recomendaciones:\n")
            for rec in r['recomendaciones']:
                text.insert("end", f"    - {rec}\n")
            
            # Separador visual entre KPAs
            text.insert("end", "\n" + "-"*80 + "\n\n")

        # Añado el resumen general al final
        text.insert("end", "\nResumen general:\n")
        text.insert("end", f"  KPAs implementadas: {resumen['implementadas']}\n")
        text.insert("end", f"  KPAs parcialmente implementadas: {resumen['parciales']}\n")
        text.insert("end", f"  KPAs deficientes: {resumen['deficientes']}\n\n")
        
        # Inserto la conclusión final sobre el cumplimiento del Nivel 2
        text.insert("end", conclusion_final(cumple_nivel2) + "\n")

        # Frame para los botones de acción
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Botón para volver al menú principal
        ttk.Button(btn_frame, text="Volver al menú", command=self.frame_inicio).pack(side="left", padx=5)
        
        # Botón para cerrar la aplicación
        ttk.Button(btn_frame, text="Cerrar", command=self.root.quit).pack(side="left", padx=5)


# --- PUNTO DE ENTRADA PRINCIPAL ---

# Este bloque solo se ejecuta si ejecuto este archivo directamente
if __name__ == "__main__":
    # Creo la ventana principal de Tkinter
    root = tk.Tk()
    
    # Instancio mi aplicación CMMI pasándole la ventana principal
    app = CMMIApp(root)
    
    # Inicio el loop de eventos de Tkinter (mantiene la ventana abierta y responde a acciones)
    root.mainloop()
