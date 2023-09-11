import tkinter as tk
from tkinter import ttk, messagebox
from img.iconos import Imagenes
import sv_ttk
from PIL import Image, ImageTk
from modules import lectura, analizador
from tabla import Ventana2

tokens_totales = []


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Ventana Principal")
        self.geometry("1066x610")

        self.resizable(0, 0)

        Contendio(self)
        sv_ttk.set_theme("dark")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Montserrat SemiBold", 12), border=0)
        self.style.configure("TButton1.TButton", foreground="#c2c3c4")
        self.style.configure("TLabel", font=("Montserrat SemiBold", 12))
        self.style.configure("FrameText.TFrame", background="#111111")
        self.configure(bg="#111111")
        # style.configure("TText", ))
        self.mainloop()


class Contendio(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(padx=40, pady=9, fill="x", side="top")
        self.style = ttk.Style()
        self.style.configure("My.TFrame", background="yellow")
        self.config(style="My.TFrame")

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
        )
        btn_3 = ttk.Button(
            panel_superior,
            text=" Reporte",
            image=self.img_report,
            compound="left",
            width=7,
            style="TButton1.TButton",
        )

        panel_superior.columnconfigure((0, 1, 2, 3), uniform="a", pad=10)
        panel_superior.rowconfigure((0), uniform="a")

        menu_button.grid(row=0, column=0, columnspan=1)
        btn_1.grid(row=0, column=1, columnspan=1)
        btn_2.grid(row=0, column=2, columnspan=1)
        btn_3.grid(row=0, column=3, columnspan=1)

    def cargar_datos(self):
        self.archivo_actual = lectura.cargar_json(self.text_area)

    def analizar_datos(self):
        texto = self.text_area.get("1.0", "end")
        # print(texto)
        if not texto.strip():
            messagebox.showerror(message="No hay información cargada", title="Error")
            return None
        analizar = analizador.Analizador()
        analizar.leer_instrucciones(texto)
        # print(analizar.tokens)
        return analizar.tokens
        # print(tokens_totales)

    def insert_tab(self, event):
        self.text_area.insert(tk.INSERT, "    ")
        return "break"

    def crear_text(self):
        panel = ttk.Frame()
        panel.pack(padx=40, pady=16, fill="both", expand=True)
        panel.config(style="FrameText.TFrame")
        self.hscrollbar = ttk.Scrollbar(panel, orient=tk.HORIZONTAL)
        self.vscrollbar = ttk.Scrollbar(panel, orient=tk.VERTICAL)

        self.text_area = tk.Text(
            panel,
            font=("Cascadia Code", 12),
            yscrollcommand=self.vscrollbar.set,
            xscrollcommand=self.hscrollbar.set,
            background="#232323",
            border=0,
        )
        self.text_area.bind("<Tab>", self.insert_tab)
        self.text_area.tag_configure("tab", tabs=("2c",))
        self.hscrollbar.config(command=self.text_area.xview)
        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vscrollbar.config(command=self.text_area.yview)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(expand=True, fill="both")

    def abrir_ventana(self):
        tokens_totales = self.analizar_datos()
        if tokens_totales:
            Ventana2(tokens_totales)

    def guardar_como(self):
        archivo = tk.filedialog.asksaveasfile(
            defaultextension=".json",
            filetypes=[("Archivos de texto", "*.json"), ("Todos los archivos", "*.*")],
        )
        if archivo:
            contenido = self.text_area.get("1.0", tk.END)
            archivo.write(contenido)
            archivo.close()

    def guardar(self):
        if self.archivo_actual:
            with open(self.archivo_actual, "w", encoding="utf-8") as archivo:
                contenido = self.text_area.get("1.0", tk.END)
                archivo.write(contenido)
        else:
            messagebox.showerror(
                message="No se ha cargado ningún archivo previamente.",
                title="Información",
            )


if __name__ == "__main__":
    App()
