from abc import ABC, abstractmethod


class Expression(ABC):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
