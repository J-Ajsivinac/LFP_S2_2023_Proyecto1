import tkinter as tk
from tkinter import ttk
from modules.Abstract.token import TipoToken
import sv_ttk


class Ventana2:
    def __init__(self, datos):
        self.ventana = tk.Toplevel()
        self.datos = datos
        self.ventana.title("Resultados")
        self.ventana.geometry("900x550")
        self.ventana.resizable(0, 0)
        # self.ventana.configure(bg="#111111")
        s = ttk.Style()
        self.ventana.configure(bg="#100f15")
        s.configure("Frame1.TFrame", background="#100f15")
        sv_ttk.set_theme("dark")
        self.style = ttk.Style()
        self.style.configure("Treeview", background="#222127")
        self.style.configure("Treeview", font=("Montserrat SemiBold", "11"))
        self.style.configure("Treeview.Heading", font=("Montserrat SemiBold", "12"))
        self.crear_contenido()

    def crear_contenido(self):
        titulo = ttk.Label(self.ventana, text="Reporte de Tokens", background="#111111")
        titulo.pack(fill="x", side="top", pady=8, padx=30)
        panel = ttk.Frame(self.ventana)
        panel.pack(padx=30, pady=2, fill="both", expand=True)
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
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=12)
        self.tabla.pack(fill="both", expand=True, pady=12)
        self.agregar_datos()

    def agregar_datos(self):
        for i, dato in enumerate(self.datos):
            valor = dato.valor
            tipo = self.mostrar_tipo(dato.tipo)
            fila = dato.fila
            columna = dato.columna
            agregar = (valor, fila, columna, tipo)
            self.tabla.insert(parent="", index=i, values=agregar)

    def mostrar_tipo(self, tipo_buscar):
        tipos = {
            TipoToken.CORCHETE_IZQ: "Corchete de Apertura",
            TipoToken.CORCHETE_DER: "Corchete de Cerradura",
            TipoToken.LLAVE_IZQ: "Llave de Apertura",
            TipoToken.LLAVE_DER: "Llave de Cerradura",
            TipoToken.COMA: "Coma",
            TipoToken.DOS_PUNTOS: "Dos Puntos",
            TipoToken.STRING: "Valor",
            TipoToken.NUMBER: "Número",
            TipoToken.O_SUMA: "Reservada Suma",
            TipoToken.O_RESTA: "Reservada Resta",
            TipoToken.O_MULTIPLICACION: "Reservada Multiplicación",
            TipoToken.O_DIVISION: "Reservada Divisíón",
            TipoToken.O_POTENCIA: "Reservada Potencia",
            TipoToken.O_RAIZ: "Reservada Raiz",
            TipoToken.O_INVERSO: "Reservada Inverso",
            TipoToken.O_SENO: "Reservada Seno",
            TipoToken.O_COSENO: "Reservada Coseno",
            TipoToken.O_TANGENTE: "Reservada Tangente",
            TipoToken.O_MOD: "Reservada Mod",
            TipoToken.PALABRA_CLAVE: "p",
            TipoToken.O_OPERACION: "Reservada Operacion",
            TipoToken.OPERACIONES: "Reservada Operaciones",
            TipoToken.CONFIGURACIONES: "Reservada Configuracione",
            TipoToken.COMILLA: "Comilla Abierta",
            TipoToken.PALABRA_CLAVE_FONDO: "Reservada Fondo",
            TipoToken.PALABRA_CLAVE_FORMA: "Reservada Forma",
            TipoToken.PALABRA_CLAVE_FUENTE: "Reservada Fuente",
            TipoToken.PALABRA_CLAVE_TEXT: "Reservada Text",
        }

        return tipos[tipo_buscar]
