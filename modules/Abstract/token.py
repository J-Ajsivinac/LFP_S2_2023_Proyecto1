from Abstract.abstract import Expression
from enum import Enum


class Token(Expression):
    def __init__(self, tipo, valor, fila, columna):
        super().__init__(fila, columna)
        self.tipo = tipo
        self.valor = valor

    def operar(self, arbol):
        return self.valor

    def getColumna(self):
        return super().getColumna()

    def getFila(self):
        return super().getFila()


class TipoToken(Enum):
    CORCHETE_IZQ = 1
    CORCHETE_DER = 2
    LLAVE_IZQ = 3
    LLAVE_DER = 4
    COMA = 5
    DOS_PUNTOS = 6
    STRING = 7
    NUMBER = 8
    O_SUMA = 9
    O_RESTA = 10
    O_MULTIPLICACION = 11
    O_DIVISION = 12
    O_POTENCIA = 13
    O_RAIZ = 14
    O_INVERSO = 15
    O_SENO = 16
    O_COSENO = 17
    O_TANGENTE = 18
    O_MOD = 19
    PALABRA_CLAVE = 20
    O_OPERACION = 21
    ERROR = 22
    OPERACIONES = 23
    CONFIGURACIONES = 24


class Estados(Enum):
    E_INICIAL = 0
    E_INICIAL_JSON = 1
    E_OPERACIONES = 2
    E_CORCHETE_I = 3
    E_OPERACION = 4
    E_VALOR1 = 5
    E_VALOR2 = 6
    E_FINAL_JSON = 3
