import tkinter as tk
from tkinter import ttk
import sv_ttk


class Ventana2:
    def __init__(self, datos):
        self.ventana = tk.Toplevel()
        self.datos = datos
        self.ventana.title("Resultados")
        self.ventana.geometry("900x550")
        self.ventana.resizable(0, 0)
        self.ventana.configure(bg="#111111")
        s = ttk.Style()
        s.configure("Frame1.TFrame", background="#111111")
        sv_ttk.set_theme("dark")
        self.crear_contenido()

    def crear_contenido(self):
        titulo = ttk.Label(self.ventana, text="Reporte de Tokens", background="#111111")
        titulo.pack(fill="x", side="top", pady=10, padx=30)
        panel = ttk.Frame(self.ventana)
        panel.pack(padx=30, pady=5, fill="both", expand=True)
        panel.configure(style="Frame1.TFrame")
        self.vscrollbar = ttk.Scrollbar(panel, orient=tk.VERTICAL)
        self.tabla = ttk.Treeview(
            panel,
            columns=("Lexema", "Fila", "Columna", "Tipo"),
            show="headings",
            yscrollcommand=self.vscrollbar.set,
        )
        self.tabla.heading("Lexema", text="Lexema")
        self.tabla.heading("Fila", text="Fila")
        self.tabla.heading("Columna", text="Columna")
        self.tabla.heading("Tipo", text="Tipo")
        # self.tabla.configure(y_scrollbar=self.vscrollbar.set)
        self.vscrollbar.config(command=self.tabla.yview)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=7)
        self.tabla.pack(fill="both", expand=True, pady=7)
        self.agregar_datos()

    def agregar_datos(self):
        for i, dato in enumerate(self.datos):
            valor = dato.valor
            tipo = dato.tipo
            fila = dato.fila
            columna = dato.columna
            agregar = (valor, fila, columna, tipo)
            self.tabla.insert(parent="", index=i, values=agregar)
