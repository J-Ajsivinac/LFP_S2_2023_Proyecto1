import tkinter as tk
from tkinter import ttk
import sv_ttk


class Ventana2:
    def __init__(self, datos):
        self.ventana = tk.Toplevel()
        self.datos = datos
        self.ventana.title("Resultados")
        self.ventana.geometry("900x500")
        self.ventana.resizable(0, 0)
        sv_ttk.set_theme("dark")
        self.crear_tabla()

    def crear_tabla(self):
        self.vscrollbar = ttk.Scrollbar(self.ventana, orient=tk.VERTICAL)
        self.tabla = ttk.Treeview(
            self.ventana,
            columns=("Lexema", "tipo"),
            show="headings",
            yscrollcommand=self.vscrollbar.set,
        )
        self.tabla.heading("Lexema", text="Lexema")
        self.tabla.heading("tipo", text="Tipo")
        # self.tabla.configure(y_scrollbar=self.vscrollbar.set)
        self.vscrollbar.config(command=self.tabla.yview)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla.pack(fill="both", expand=True)
        self.agregar_datos()

    def agregar_datos(self):
        for i, dato in enumerate(self.datos):
            valor = dato.valor
            tipo = dato.tipo
            agregar = (valor, tipo)
            self.tabla.insert(parent="", index=i, values=agregar)
