# diagnostico_cmmi_tkinter.py
import tkinter as tk
from tkinter import ttk, messagebox
from KPAS import KPAS
from VALOR_RESPUESTA import VALOR_RESPUESTA
from RECOMENDACIONES_BASE import RECOMENDACIONES_BASE
from porcentaje import estado_porcentaje
import datetime


# --- LÓGICA (adaptada) ---

def generar_recomendaciones_por_respuestas(kpa, respuestas_raw):
    lista = []
    problemas = [r for r in respuestas_raw if r['opcion'] in ('2', '3')]
    if problemas:
        lista.extend(RECOMENDACIONES_BASE.get(kpa, []))
        for r in problemas:
            texto_preg = r['pregunta']
            if r['opcion'] == '3':
                lista.append(f"'{texto_preg}' → No implementado. Priorizar su corrección.")
            elif r['opcion'] == '2':
                lista.append(f"'{texto_preg}' → Parcialmente implementado. Mejorar formalidad.")
    else:
        lista.append("Todas las prácticas clave parecen estar satisfechas. Mantener procesos y evidencias.")
    # Evitar duplicados manteniendo orden
    visto = set()
    salida = []
    for contenido in lista:
        if contenido not in visto:
            salida.append(contenido)
            visto.add(contenido)
    return salida


def evaluar_kpa(nombre_kpa, respuestas_usuario):
    """
    Evalúa una KPA recibiendo una lista de respuestas del usuario en formato de opciones '1','2','3'.
    Devuelve dict con kpa, porcentaje, estado, respuestas (detalladas) y recomendaciones.
    """
    preguntas = KPAS[nombre_kpa]
    respuestas_raw = []
    valores = []

    for p, opcion in zip(preguntas, respuestas_usuario):
        # VALOR_RESPUESTA debe mapear '1'->valor_numérico, '2'->..., '3'->...
        val = VALOR_RESPUESTA[opcion]
        respuestas_raw.append({
            "pregunta": p,
            "opcion": opcion,
            "valor": val,
            "texto": {"1": "Sí", "2": "Parcial", "3": "No"}[opcion]
        })
        valores.append(val)

    porcentaje = (sum(valores) / len(valores)) * 100 if valores else 0
    estado = estado_porcentaje(porcentaje)
    recomendaciones = generar_recomendaciones_por_respuestas(nombre_kpa, respuestas_raw)

    return {
        "kpa": nombre_kpa,
        "porcentaje": round(porcentaje, 2),
        "estado": estado,
        "respuestas": respuestas_raw,
        "recomendaciones": recomendaciones
    }


def generar_resumen_general(resultados):
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
    cumple_nivel2 = (resumen["implementadas"] == len(KPAS))
    return resumen, cumple_nivel2


def conclusion_final(cumple_nivel2):
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if cumple_nivel2:
        mensaje = f"Conclusión ({ahora}): El proyecto cumple el Nivel 2 de CMMI."
    else:
        mensaje = f"Conclusión ({ahora}): El proyecto NO cumple el Nivel 2 de CMMI. Recomendado trabajar las áreas deficientes y parciales."
    return mensaje


# --- INTERFAZ TKINTER ---

class CMMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diagnóstico CMMI Nivel 2")
        self.root.geometry("920x700")

        self.nombre_proyecto = tk.StringVar()
        self.kpa_actual = None

        # Variables para evaluación por lotes (evaluar todas)
        self.batch_kpas = []
        self.batch_index = 0
        self.batch_results = []

        self.frame_inicio()

    def limpiar_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def frame_inicio(self):
        self.limpiar_frame()
        tk.Label(self.root, text="Herramienta Diagnóstico CMMI Nivel 2",
                 font=("Helvetica", 18, "bold")).pack(pady=20)
        tk.Label(self.root, text="Nombre del proyecto:").pack()
        tk.Entry(self.root, textvariable=self.nombre_proyecto, width=60).pack(pady=5)
        ttk.Button(self.root, text="Evaluar todas las KPAs", command=self.evaluar_todas).pack(pady=10)
        ttk.Button(self.root, text="Evaluar una KPA específica", command=self.menu_kpa).pack(pady=10)
        ttk.Button(self.root, text="Salir", command=self.root.quit).pack(pady=10)

    def menu_kpa(self):
        self.limpiar_frame()
        tk.Label(self.root, text="Selecciona una KPA:", font=("Helvetica", 14, "bold")).pack(pady=20)
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, height=420)

        for kpa in KPAS.keys():
            ttk.Button(scroll_frame, text=kpa, width=80,
                       command=lambda k=kpa: self.formulario_kpa(k)).pack(pady=5)

        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y")
        ttk.Button(self.root, text="Volver", command=self.frame_inicio).pack(pady=10)

    # --- Evaluar una sola KPA ---
    def formulario_kpa(self, kpa):
        self.limpiar_frame()
        self.kpa_actual = kpa
        tk.Label(self.root, text=f"KPA: {kpa}", font=("Helvetica", 16, "bold")).pack(pady=10)
        preguntas = KPAS[kpa]

        self.vars = []
        frame_preguntas = ttk.Frame(self.root)
        frame_preguntas.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(frame_preguntas)
        scrollbar = ttk.Scrollbar(frame_preguntas, orient="vertical", command=canvas.yview)
        preguntas_frame = ttk.Frame(canvas)

        preguntas_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=preguntas_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, height=420)

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

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Evaluar", command=self.mostrar_resultado_kpa).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Volver", command=self.menu_kpa).pack(side="left")

    def mostrar_resultado_kpa(self):
        respuestas_usuario = [v.get() for v in self.vars]
        if "" in respuestas_usuario:
            messagebox.showerror("Error", "Responde todas las preguntas antes de continuar.")
            return
        resultado = evaluar_kpa(self.kpa_actual, respuestas_usuario)
        self.mostrar_informe(resultado, volver_menu=True)

    def mostrar_informe(self, resultado, volver_menu=False):
        self.limpiar_frame()
        tk.Label(self.root, text=f"Informe de {resultado['kpa']}",
                 font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(self.root, text=f"Cumplimiento: {resultado['porcentaje']}%").pack()
        tk.Label(self.root, text=f"Estado: {resultado['estado']}").pack(pady=5)

        frame_texto = ttk.Frame(self.root)
        frame_texto.pack(fill="both", expand=True, padx=20, pady=10)
        text = tk.Text(frame_texto, wrap="word")
        text.pack(fill="both", expand=True, side="left")
        scroll = ttk.Scrollbar(frame_texto, command=text.yview, orient="vertical")
        scroll.pack(side="right", fill="y")
        text.configure(yscrollcommand=scroll.set)

        text.insert("end", "Respuestas:\n\n")
        for r in resultado["respuestas"]:
            text.insert("end", f" - {r['pregunta']}\n     → {r['texto']}\n")
        text.insert("end", "\nRecomendaciones:\n\n")
        for rec in resultado["recomendaciones"]:
            text.insert("end", f" - {rec}\n")

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        if volver_menu:
            ttk.Button(btn_frame, text="Volver al menú", command=self.frame_inicio).pack()
        else:
            ttk.Button(btn_frame, text="Volver al menú", command=self.frame_inicio).pack()
        # también dejamos la opción de guardar si se quiere (por extensión)

    # --- Evaluar todas las KPAs (batch) ---
    def evaluar_todas(self):
        # Inicializa el proceso de evaluación secuencial de todas las KPAs
        self.batch_kpas = list(KPAS.keys())
        self.batch_index = 0
        self.batch_results = []
        if not self.batch_kpas:
            messagebox.showinfo("Info", "No hay KPAs definidas.")
            return
        # preguntar confirmación (opcional)
        if messagebox.askyesno("Confirmar", "Se van a evaluar todas las KPAs de forma secuencial. ¿Continuar?"):
            self.formulario_kpa_batch(self.batch_index)

    def formulario_kpa_batch(self, index):
        # Si hemos terminado todas, mostramos resumen
        if index >= len(self.batch_kpas):
            self.mostrar_resumen_general(self.batch_results)
            return

        self.limpiar_frame()
        kpa = self.batch_kpas[index]
        self.kpa_actual = kpa
        tk.Label(self.root, text=f"KPA [{index+1}/{len(self.batch_kpas)}]: {kpa}", font=("Helvetica", 16, "bold")).pack(pady=10)
        preguntas = KPAS[kpa]

        self.vars = []
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

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Guardar y Siguiente", command=self.guardar_siguiente_batch).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar (volver al menú)", command=self.cancelar_batch).pack(side="left", padx=5)

    def guardar_siguiente_batch(self):
        respuestas_usuario = [v.get() for v in self.vars]
        if "" in respuestas_usuario:
            messagebox.showerror("Error", "Responde todas las preguntas antes de continuar.")
            return
        resultado = evaluar_kpa(self.kpa_actual, respuestas_usuario)
        self.batch_results.append(resultado)
        self.batch_index += 1
        # Avanzar a la siguiente KPA o terminar
        self.formulario_kpa_batch(self.batch_index)

    def cancelar_batch(self):
        if messagebox.askyesno("Confirmar", "Cancelar evaluación de todas las KPAs y volver al menú?"):
            self.batch_kpas = []
            self.batch_index = 0
            self.batch_results = []
            self.frame_inicio()

    def mostrar_resumen_general(self, resultados):
        self.limpiar_frame()
        tk.Label(self.root, text="INFORME RESUMIDO (todas las KPAs)", font=("Helvetica", 16, "bold")).pack(pady=10)

        resumen, cumple_nivel2 = generar_resumen_general(resultados)

        frame_texto = ttk.Frame(self.root)
        frame_texto.pack(fill="both", expand=True, padx=20, pady=10)
        text = tk.Text(frame_texto, wrap="word")
        text.pack(fill="both", expand=True)
        scroll = ttk.Scrollbar(frame_texto, command=text.yview, orient="vertical")
        scroll.pack(side="right", fill="y")
        text.configure(yscrollcommand=scroll.set)

        for r in resultados:
            text.insert("end", f"KPA: {r['kpa']}\n")
            text.insert("end", f" - Cumplimiento: {r['porcentaje']}%\n")
            text.insert("end", f" - Estado: {r['estado']}\n")
            text.insert("end", " - Respuestas:\n")
            for resp in r['respuestas']:
                text.insert("end", f"    * {resp['pregunta']} → {resp['texto']}\n")
            text.insert("end", " - Recomendaciones:\n")
            for rec in r['recomendaciones']:
                text.insert("end", f"    - {rec}\n")
            text.insert("end", "\n" + "-"*80 + "\n\n")

        text.insert("end", "\nResumen general:\n")
        text.insert("end", f"  KPAs implementadas: {resumen['implementadas']}\n")
        text.insert("end", f"  KPAs parcialmente implementadas: {resumen['parciales']}\n")
        text.insert("end", f"  KPAs deficientes: {resumen['deficientes']}\n\n")
        text.insert("end", conclusion_final(cumple_nivel2) + "\n")

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Volver al menú", command=self.frame_inicio).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cerrar", command=self.root.quit).pack(side="left", padx=5)


# --- MAIN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CMMIApp(root)
    root.mainloop()
