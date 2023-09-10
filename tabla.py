import tkinter as tk
from tkinter import ttk
import sv_ttk


class Ventana2:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("Resultados")
        self.ventana.geometry("900x500")
        self.ventana.resizable(0, 0)
        sv_ttk.set_theme("dark")
        self.crear_tabla()

    def crear_tabla(self):
        self.tabla = ttk.Treeview(
            self.ventana, columns=("Lexema", "tipo"), show="headings"
        )
        self.tabla.heading("Lexema", text="Lexema")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.pack(fill="both", expand=True)
        self.agregar_datos()

    def agregar_datos(self):
        lexema = 1
        tipo = 2
        data = (lexema, tipo)
        self.tabla.insert(parent="", index=0, values=data)
