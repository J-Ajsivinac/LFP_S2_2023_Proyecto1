import tkinter as tk
from tkinter import ttk, messagebox
from img.iconos import Imagenes
import sv_ttk
from PIL import Image, ImageTk
from modules import lectura, analizador, instrucciones
from tabla import Ventana2
import copy
import json
import os


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana Principal")
        self.geometry("1066x610")
        self.resizable(0, 0)
        sv_ttk.set_theme("dark")

        Contendio(self)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Montserrat SemiBold", 12), border=0)
        self.style.configure("TButton1.TButton", foreground="#c2c3c4")
        self.style.configure("TLabel", font=("Montserrat SemiBold", 12))
        self.style.configure("FrameText.TFrame", background="#111111")
        self.configure(bg="#100f15")
        # style.configure("TText", ))
        self.mainloop()


class Contendio(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(padx=40, pady=9, fill="x", side="top")
        self.style = ttk.Style()
        self.style.configure("My.TFrame")
        self.config(style="My.TFrame")
        self.errores = []
        self.tokens_totales = []
        self.crear_menu_superior()
        self.crear_text()
        self.archivo_actual = None

    def crear_menu_superior(self):
        panel_superior = tk.Frame()
        panel_superior.pack(padx=7, pady=3, fill="x", side="top")
        panel_superior.configure(bg="#111111")
        img = Image.open(Imagenes.BTN_SCANNER)
        img = img.resize((20, 18), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(img)

        img_error = Image.open(Imagenes.BTN_ERROR)
        img_error = img_error.resize((20, 18), Image.LANCZOS)
        self.img_error = ImageTk.PhotoImage(img_error)

        img_home = Image.open(Imagenes.BTN_HOME)
        img_home = img_home.resize((20, 18), Image.LANCZOS)
        self.img_home = ImageTk.PhotoImage(img_home)

        img_report = Image.open(Imagenes.BTN_REPORT)
        img_report = img_report.resize((20, 18), Image.LANCZOS)
        self.img_report = ImageTk.PhotoImage(img_report)
        menu_button = ttk.Menubutton(
            panel_superior, text="", image=self.img_home, compound="left", width=1
        )
        # menu_button.configure(borderwidth=0)

        # menu_button["borderwidth"] = 0
        button_sub_menu = tk.Menu(
            menu_button,
            tearoff=False,
            relief=tk.SOLID,
            font=("Montserrat", 12),
            borderwidth=20,
        )
        # button_sub_menu["borderwidth"] = 0
        button_sub_menu.add_command(label="  Abrir", command=self.cargar_datos)
        button_sub_menu.add_command(label="  Guardar", command=self.guardar)
        button_sub_menu.add_command(label="  Guardar Como", command=self.guardar_como)
        button_sub_menu.add_command(label="  Salir", command=self.parent.destroy)

        menu_button["menu"] = button_sub_menu
        btn_1 = ttk.Button(
            panel_superior,
            image=self.img,
            text=" Analizar",
            compound="left",
            width=7,
            command=self.abrir_ventana,
            style="TButton1.TButton",
        )
        btn_1.grid_configure(padx=0)
        # btn_1.configure(foreground="#50dfea")
        btn_2 = ttk.Button(
            panel_superior,
            image=self.img_error,
            text=" Errores",
            compound="left",
            width=7,
            style="TButton1.TButton",
            command=self.crear_archivo_error,
        )
        btn_3 = ttk.Button(
            panel_superior,
            text=" Reporte",
            image=self.img_report,
            compound="left",
            width=7,
            style="TButton1.TButton",
            command=self.crear_reporte,
        )

        panel_superior.columnconfigure((0, 1, 2, 3), uniform="a", pad=10)
        panel_superior.rowconfigure((0), uniform="a")

        menu_button.grid(row=0, column=0, columnspan=1)
        btn_1.grid(row=0, column=1, columnspan=1)
        btn_2.grid(row=0, column=2, columnspan=1)
        btn_3.grid(row=0, column=3, columnspan=1)

    def insert_tab(self, event):
        self.text_area.insert(tk.INSERT, "    ")
        return "break"

    def actualizar_contador(self, event=None):
        codigo_lineas = self.text_area.get("1.0", "end-1c").split("\n")
        num_lineas = len(codigo_lineas) + 1
        self.contador.config(state="normal")
        self.contador.delete(1.0, "end")
        for i in range(1, num_lineas):
            if i == (num_lineas - 1):
                self.contador.insert("end", f"{i}")
            else:
                self.contador.insert("end", f"{i}\n")

        self.contador.config(state="disabled")

        tempo = self.text_area.yview()
        self.contador.yview_moveto(tempo[0])

    def sync_scrollbars(self, *args):
        # Cuando se desplaza el scrollbar, se actualizan las posiciones de los widgets Text
        self.text_area.yview(*args)
        self.contador.yview(*args)

    def bloquear_scroll(self, event):
        return "break"

    def sync_text_widgets(self, *args):
        # Cuando se desplaza uno de los widgets Text, se actualiza la posición del scrollbar y del otro widget Text
        self.contador.yview_moveto(args[0])
        self.vscrollbar.set(*args)

    def crear_text(self):
        panel = ttk.Frame()
        panel.pack(padx=40, pady=16, fill="both", expand=True)
        panel.config(style="FrameText.TFrame")
        self.nombre_archivo = tk.Label(
            panel,
            text="Nuevo Documento.json",
            background="#323445",
            font=("Montserrat SemiBold", 11),
            foreground="#979CD1",
        )
        self.nombre_archivo.pack(fill="x")
        self.hscrollbar = ttk.Scrollbar(panel, orient=tk.HORIZONTAL)
        self.vscrollbar = ttk.Scrollbar(panel, orient=tk.VERTICAL)
        self.contador = tk.Text(
            panel,
            font=("Cascadia Code", 12),
            width=5,
            border=0,
            state="disabled",
            background="#28272f",
            yscrollcommand=self.vscrollbar.set,
        )
        # self.contador.configure(state="normal")
        # self.contador.insert("1.0", "1")
        # self.contador.configure(state="disabled")

        self.contador.bind(
            "<MouseWheel>", self.bloquear_scroll
        )  # Bloquea el desplazamiento con la rueda del ratón
        self.contador.bind(
            "<Up>", self.bloquear_scroll
        )  # Bloquea el desplazamiento hacia arriba con la tecla flecha arriba
        self.contador.bind("<Down>", self.bloquear_scroll)

        self.text_area = tk.Text(
            panel,
            font=("Cascadia Code", 12),
            yscrollcommand=self.vscrollbar.set,
            xscrollcommand=self.hscrollbar.set,
            background="#222127",
            border=0,
            wrap="none",
        )
        self.text_area.bind("<Tab>", self.insert_tab)
        self.text_area.tag_configure("tab", tabs=("2c",))
        self.hscrollbar.config(command=self.text_area.xview)
        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.contador.pack(side=tk.LEFT, fill="y")

        self.vscrollbar.config(command=self.sync_scrollbars)
        self.text_area.config(yscrollcommand=self.sync_text_widgets)
        # self.contador.config(yscrollcommand=self.sync_text_widgets)

        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(expand=True, fill="both")
        self.text_area.bind("<KeyRelease>", self.actualizar_contador)
        # self.text_area.bind("<BackSpace>", self.actualizar_c)
        self.actualizar_contador(None)

    def cargar_datos(self):
        self.archivo_actual = lectura.cargar_json(self.text_area)
        if self.archivo_actual:
            _, nombre = os.path.split(self.archivo_actual)
            self.nombre_archivo.config(text=nombre)
            self.actualizar_contador()

    def analizar_datos(self):
        texto = self.text_area.get("1.0", "end")
        # print(texto)
        if not texto.strip():
            messagebox.showerror(message="No hay información cargada", title="Error")
            return None
        analizar = analizador.Analizador()
        analizar.leer_instrucciones(texto.lower())
        # print(analizar.tokens)
        self.errores = copy.deepcopy(analizar.errores)
        self.tokens_totales = copy.deepcopy(analizar.tokens)
        # print(tokens_totales)

    def crear_archivo_error(self):
        if self.tokens_totales:
            json_error = {"errores": []}
            for error in self.errores:
                error_dict = {
                    "No": error.numero,
                    "descripcion": {
                        "lexema": error.lexema,
                        "tipo": error.tipo,
                        "columna": error.columna,
                        "fila": error.fila,
                    },
                }
                json_error["errores"].append(error_dict)
            json_data = json.dumps(json_error, indent=4, ensure_ascii=False)
            with open("errores.json", "w", encoding="utf-8") as json_file:
                json_file.write(json_data)
            os.system("start errores.json")
            # messagebox.showinfo(message="Archivo de errores Creado", title="Éxito")
        else:
            messagebox.showerror(message="No hay datos analizados", title="Error")

    def crear_reporte(self):
        if self.tokens_totales:
            i = instrucciones.Instrucciones(self.tokens_totales)
            i.iniciar()
        else:
            messagebox.showerror(message="No hay datos analizados", title="Error")

    def abrir_ventana(self):
        self.analizar_datos()
        if self.tokens_totales:
            Ventana2(self.tokens_totales)

    def guardar_como(self):
        archivo = tk.filedialog.asksaveasfile(
            defaultextension=".json",
            filetypes=[("Archivos de texto", "*.json"), ("Todos los archivos", "*.*")],
        )
        if archivo:
            self.archivo_actual = archivo.name
            print(self.archivo_actual)
            contenido = self.text_area.get("1.0", tk.END)
            archivo.write(contenido)
            archivo.close()
            _, nombre = os.path.split(self.archivo_actual)
            self.nombre_archivo.config(text=nombre)

    def guardar(self):
        if self.archivo_actual:
            with open(self.archivo_actual, "w", encoding="UTF-8") as archivo:
                contenido = self.text_area.get("1.0", tk.END)
                archivo.write(contenido)
                messagebox.showinfo(message="Archivo Guardado", title="Éxito")
        else:
            messagebox.showerror(
                message="No se ha cargado ningún archivo previamente.",
                title="Información",
            )


if __name__ == "__main__":
    App()
