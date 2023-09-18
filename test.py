import tkinter as tk
from tkinter import ttk


def actualizar_contador(event):
    codigo_lineas = codigo.get("1.0", "end-1c").split("\n")
    num_lineas = len(codigo_lineas)
    contador.config(state="normal")
    contador.delete(1.0, "end")
    for i in range(1, num_lineas + 1):
        contador.insert("end", f"{i}\n")
    contador.config(state="disabled")


def on_codigo_scroll(*args):
    codigo.yview(*args)
    contador.yview(*args)


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Editor de Código con Contador de Líneas")
ventana.geometry("400x400")
# Widget Text para el contador de líneas
contador = tk.Text(ventana, width=4, wrap=tk.NONE)
contador.pack(side="left", fill="y")
contador.config(state="disabled")
# Widget Text para el código
codigo_frame = ttk.Frame(ventana)
codigo_frame.pack(fill="both", expand=True)

codigo_scrollbar = ttk.Scrollbar(
    codigo_frame, orient="vertical", command=on_codigo_scroll
)
codigo = tk.Text(codigo_frame, wrap=tk.NONE, yscrollcommand=codigo_scrollbar.set)
codigo_scrollbar.pack(side="right", fill="y")
codigo.pack(fill="both", expand=True)
codigo.bind("<KeyRelease>", actualizar_contador)


# Configurar el desplazamiento sincronizado
contador_scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=on_codigo_scroll)
contador_scrollbar.pack(side="left", fill="y")
contador.config(yscrollcommand=contador_scrollbar.set)

# Inicializar el contador de líneas
actualizar_contador(None)

# Ejecutar la aplicación
ventana.mainloop()
