import os


class Imagenes:
    _ruta = os.path.dirname(os.path.abspath(__file__))
    BTN_ANALIZAR = os.path.join(_ruta, "lupa.png").replace("\\", "\\\\")
    BTN_HOME = os.path.join(_ruta, "home.png").replace("\\", "\\\\")
    BTN_SCANNER = os.path.join(_ruta, "scanner.png").replace("\\", "\\\\")
    BTN_ERROR = os.path.join(_ruta, "error.png").replace("\\", "\\\\")
    BTN_REPORT = os.path.join(_ruta, "graph.png").replace("\\", "\\\\")
