class Error:
    def __init__(self, tipo, fila, columna, lexema):
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.lexema = lexema
