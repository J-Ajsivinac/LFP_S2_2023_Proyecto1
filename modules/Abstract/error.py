from modules.Abstract.abstract import Expression


class Error(Expression):
    def __init__(self, numero, tipo, fila, columna, lexema):
        super().__init__(fila, columna)
        self.numero = numero
        self.tipo = tipo
        self.lexema = lexema
