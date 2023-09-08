import tkinter as tk
from tkinter import ttk
from img.iconos import Imagenes
import sv_ttk
from PIL import Image, ImageTk
from modules.lectura import load_json


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana Principal")
        self.geometry("1066x600")

        self.resizable(0, 0)

        Contendio(self)
        sv_ttk.set_theme("dark")

        style = ttk.Style()
        style.configure("TButton", font=("Montserrat", 12))
        style.configure("TLabel", font=("Montserrat", 12))
        self.configure(bg="#111111")
        # style.configure("TText", ))
        self.mainloop()


class Contendio(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(padx=40, pady=10, fill="x", side="top")
        style = ttk.Style()
        style.configure("My.TFrame", background="yellow")
        self.config(style="My.TFrame")

        self.crear_menu_superior()
        self.crear_text()

    def crear_menu_superior(self):
        panel_superior = tk.Frame()
        panel_superior.pack(padx=7, pady=1, fill="x", side="top")
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

        button_sub_menu = tk.Menu(
            menu_button, tearoff=False, relief=tk.FLAT, bd=0, font=("Montserrat", 12)
        )
        button_sub_menu.add_command(label="Abrir", command=self.on_button_click)
        button_sub_menu.add_command(label="Guardar")
        button_sub_menu.add_command(label="Guardar Como")
        button_sub_menu.add_command(label="Salir", command=self.parent.destroy)

        menu_button["menu"] = button_sub_menu

        btn_1 = ttk.Button(
            panel_superior,
            image=self.img,
            text="  Analizar",
            compound="left",
            width=7,
        )
        btn_1.grid_configure(padx=0)

        btn_2 = ttk.Button(
            panel_superior,
            image=self.img_error,
            text="  Errores",
            compound="left",
            width=7,
        )
        btn_3 = ttk.Button(
            panel_superior,
            text="  Reporte",
            image=self.img_report,
            compound="left",
            width=7,
        )

        panel_superior.columnconfigure((0, 1, 2, 3), uniform="a", pad=10)
        panel_superior.rowconfigure((0), uniform="a")

        menu_button.grid(row=0, column=0, columnspan=1)
        btn_1.grid(row=0, column=1, columnspan=1)
        btn_2.grid(row=0, column=2, columnspan=1)
        btn_3.grid(row=0, column=3, columnspan=1)

    def on_button_click(self):
        load_json(self.text_area)

    def insert_tab(self, event):
        self.text_area.insert(tk.INSERT, "    ")
        return "break"

    def crear_text(self):
        panel = ttk.Frame()
        panel.pack(padx=40, pady=14, fill="both", expand=True)
        self.hscrollbar = ttk.Scrollbar(panel, orient=tk.HORIZONTAL)
        self.vscrollbar = ttk.Scrollbar(panel, orient=tk.VERTICAL)
        style = ttk.Style()
        style.configure(
            "Custom.TText", background="white", borderwidth=1, relief="solid"
        )

        self.text_area = tk.Text(
            panel,
            font=("Cascadia Code", 12),
            yscrollcommand=self.vscrollbar.set,
            xscrollcommand=self.hscrollbar.set,
            background="#252525",
        )
        self.text_area.bind("<Tab>", self.insert_tab)
        self.text_area.tag_configure("tab", tabs=("2c",))
        self.hscrollbar.config(command=self.text_area.xview)
        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vscrollbar.config(command=self.text_area.yview)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(expand=True, fill="both")


if __name__ == "__main__":
    App()
