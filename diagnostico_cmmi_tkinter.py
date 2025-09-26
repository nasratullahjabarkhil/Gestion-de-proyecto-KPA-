import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from KPAS import KPAS
from VALOR_RESPUESTA import VALOR_RESPUESTA
from RECOMENDACIONES_BASE import RECOMENDACIONES_BASE
from porcentaje import estado_porcentaje

class DiagnosticoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diagnóstico CMMI Nivel 2")
        self.root.geometry("800x600")

        # Proyecto
        tk.Label(root, text="Nombre del proyecto:").pack(anchor="w", padx=10, pady=5)
        self.proyecto_var = tk.StringVar()
        tk.Entry(root, textvariable=self.proyecto_var, width=40).pack(anchor="w", padx=10)

        # Selector de KPA
        tk.Label(root, text="Selecciona la KPA a evaluar:").pack(anchor="w", padx=10, pady=5)
        self.kpa_var = tk.StringVar(value=list(KPAS.keys())[0])
        ttk.Combobox(root, textvariable=self.kpa_var, values=list(KPAS.keys()), state="readonly", width=40).pack(anchor="w", padx=10)

        # Botón de iniciar
        tk.Button(root, text="Iniciar evaluación", command=self.iniciar_evaluacion, fg="black").pack(pady=10)

        # Frame de preguntas
        self.frame_preguntas = tk.Frame(root)
        self.frame_preguntas.pack(fill="both", expand=True, padx=10, pady=10)

        # Texto de resultados
        self.text_resultado = tk.Text(root, height=15, wrap="word")
        self.text_resultado.pack(fill="both", expand=True, padx=10, pady=10)

    def iniciar_evaluacion(self):
         # Comprobar si el nombre del proyecto está vacío
        if not self.proyecto_var.get().strip():
            messagebox.showerror("Error", "El nombre del proyecto no puede estar vacío.")
            return  # Salimos y no seguimos con la evaluación
        
        # Limpia resultados previos
        for widget in self.frame_preguntas.winfo_children():
            widget.destroy()
        self.respuestas = {}
        kpa = self.kpa_var.get()
        preguntas = KPAS[kpa]

        tk.Label(self.frame_preguntas, text=f"Evaluando: {kpa}", font=("Arial", 14, "bold")).pack(pady=5)
        for i, p in enumerate(preguntas, 1):
            frame = tk.Frame(self.frame_preguntas)
            frame.pack(anchor="w", pady=3, fill="x")
            tk.Label(frame, text=f"{i}. {p}", anchor="w").pack(side="left")
            var = tk.StringVar(value="Sí")
            self.respuestas[p] = var
            for opcion, valor in [("Sí", "1"), ("Parcial", "2"), ("No", "3")]:
                tk.Radiobutton(frame, text=opcion, variable=var, value=valor).pack(side="left", padx=5)


        tk.Button(self.frame_preguntas, text="Calcular diagnóstico", command=self.calcular_diagnostico, fg="black").pack(pady=10)

    def calcular_diagnostico(self):
        kpa = self.kpa_var.get()
        respuestas = [VALOR_RESPUESTA[self.respuestas[p].get()] for p in KPAS[kpa]]
        porcentaje = (sum(respuestas) / len(respuestas)) * 100
        estado = estado_porcentaje(porcentaje)

        # Generar recomendaciones
        recomendaciones = []
        if estado != "Implementada":
            recomendaciones = RECOMENDACIONES_BASE[kpa]

        # Mostrar resultados
        self.text_resultado.delete("1.0", tk.END)
        self.text_resultado.insert(tk.END, f"Proyecto: {self.proyecto_var.get() or 'Sin nombre'}\n")
        self.text_resultado.insert(tk.END, f"KPA evaluada: {kpa}\n")
        self.text_resultado.insert(tk.END, f"Cumplimiento: {porcentaje:.2f}%\n")
        self.text_resultado.insert(tk.END, f"Estado: {estado}\n\n")
        self.text_resultado.insert(tk.END, "Recomendaciones:\n")
        if recomendaciones:
            for rec in recomendaciones:
                self.text_resultado.insert(tk.END, f" - {rec}\n")
        else:
            self.text_resultado.insert(tk.END, " - Todas las prácticas clave están implementadas.\n")

        self.text_resultado.insert(tk.END, "\nFecha de diagnóstico: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagnosticoApp(root)
    root.mainloop()
