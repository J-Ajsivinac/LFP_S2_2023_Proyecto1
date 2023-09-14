class Error:
    def __init__(self, numero, tipo, fila, columna, lexema):
        self.numero = numero
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.lexema = lexema
