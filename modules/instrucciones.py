from modules.Abstract.token import Token, TipoToken
from modules.graph import Graph
import math
import copy
from tkinter import ttk, messagebox


class Instrucciones:
    def __init__(self, tokens):
        self.tokens = tokens
        self.instrucciones = []
        self.temp = []
        self.configuraciones = {
            TipoToken.PALABRA_CLAVE_TEXT: None,
            TipoToken.PALABRA_CLAVE_FONDO: None,
            TipoToken.PALABRA_CLAVE_FUENTE: None,
            TipoToken.PALABRA_CLAVE_FORMA: None,
        }

    def operar(self, indice=0, recursivo=False):
        valores = []
        op = None
        # self.i = indice + 1
        ind = indice
        while self.tokens:
            lexema = self.tokens.pop(0)
            if lexema.tipo in [
                TipoToken.O_INVERSO,
                TipoToken.O_SENO,
                TipoToken.O_COSENO,
                TipoToken.O_TANGENTE,
                TipoToken.O_SUMA,
                TipoToken.O_RESTA,
                TipoToken.O_MULTIPLICACION,
                TipoToken.O_DIVISION,
                TipoToken.O_POTENCIA,
                TipoToken.O_RAIZ,
                TipoToken.O_MOD,
            ]:
                op = lexema
                break
            elif lexema.tipo in [
                TipoToken.PALABRA_CLAVE_FONDO,
                TipoToken.PALABRA_CLAVE_FORMA,
                TipoToken.PALABRA_CLAVE_FUENTE,
                TipoToken.PALABRA_CLAVE_TEXT,
            ]:
                tipo = lexema
                temp = self.tokens.pop(0)
                while temp.tipo in [
                    TipoToken.COMILLA,
                    TipoToken.DOS_PUNTOS,
                ]:
                    temp = self.tokens.pop(0)
                if temp.tipo in [TipoToken.STRING, TipoToken.OPERACIONES]:
                    self.configuraciones[tipo.tipo] = temp.valor

        if not op:
            return
        self.temp.append(op.valor + "\n")
        iterador = len(self.temp) - 1
        while self.tokens:
            lexema = self.tokens.pop(0)
            if lexema.tipo == TipoToken.STRING:
                if self.tokens[0].tipo == TipoToken.STRING:
                    continue
                temp = self.tokens.pop(0)
                while temp.tipo in [
                    TipoToken.COMILLA,
                    TipoToken.DOS_PUNTOS,
                    TipoToken.CORCHETE_IZQ,
                ]:
                    temp = self.tokens.pop(0)
                valor = temp
                if valor.tipo == TipoToken.LLAVE_IZQ:
                    self.temp.append(valor.valor)
                    valores.append(self.operar(ind + 1, True))
                else:
                    if valor.tipo == TipoToken.NUMBER:
                        if op.tipo in [
                            TipoToken.O_SENO,
                            TipoToken.O_COSENO,
                            TipoToken.O_TANGENTE,
                            TipoToken.O_INVERSO,
                        ]:
                            if len(valores) == 0:
                                self.temp.append(valor.valor)
                                valores.append(valor.valor)
                        else:
                            self.temp.append(valor.valor)
                            valores.append(valor.valor)

            if lexema.tipo in [TipoToken.LLAVE_DER]:
                self.temp.append(lexema.valor)
            if lexema.tipo == TipoToken.CORCHETE_DER:
                if recursivo:
                    lexema = self.tokens.pop(0)
                    if lexema.tipo == TipoToken.LLAVE_DER:
                        self.temp.append(lexema.valor)
                        break
                break
            if lexema.tipo == TipoToken.O_OPERACION:
                break
        if len(valores) == 0 and len(self.tokens) == 0 and not op:
            return None
        regresar = None
        if op.tipo == TipoToken.O_SUMA:
            regresar = sum(valores)
        elif op.tipo == TipoToken.O_RESTA:
            regresar = valores[0] - sum(valores[1:])
        elif op.tipo == TipoToken.O_MULTIPLICACION:
            result = 1
            for valor in valores:
                result *= valor
            regresar = result
        elif op.tipo == TipoToken.O_DIVISION:
            if valores[1] != 0:
                regresar = valores[0] / valores[1]
            else:
                regresar = valores[0] / 1
                messagebox.showerror(
                    message="División por 0 no aceptada\nValor por defecto = 1",
                    title="Error",
                )

        elif op.tipo == TipoToken.O_POTENCIA:
            regresar = math.pow(valores[0], valores[1])
        elif op.tipo == TipoToken.O_RAIZ:
            if valores[1] != 0:
                regresar = math.pow(valores[0], 1 / valores[1])
            else:
                regresar = math.pow(valores[0], 1)
                messagebox.showerror(
                    message="División por 0 no aceptada\nValor por defecto = 1",
                    title="Error",
                )

        elif op.tipo == TipoToken.O_INVERSO:
            if valores[0] != 0:
                regresar = 1 / valores[0]
            else:
                messagebox.showerror(
                    message="División por 0 no aceptada\nValor por defecto = 1",
                    title="Error",
                )

                regresar = 1
        elif op.tipo == TipoToken.O_SENO:
            regresar = math.sin(math.radians(valores[0]))
        elif op.tipo == TipoToken.O_COSENO:
            regresar = math.cos(math.radians(valores[0]))
        elif op.tipo == TipoToken.O_TANGENTE:
            regresar = math.tan(math.radians(valores[0]))
        elif op.tipo == TipoToken.O_MOD:
            regresar = valores[0] % valores[1]
        else:
            print(f"Operación no soportada: {op}")
        valores.reverse()

        self.temp[iterador] += str(regresar)

        return regresar

    def iniciar(self):
        operacion = ""

        while True:
            operacion = self.operar()
            if operacion is not None:
                self.instrucciones.append(copy.deepcopy(self.temp))
            else:
                break
            self.temp.clear()
        self.llamar_grafica()

    def llamar_grafica(self):
        grafica = Graph(self.configuraciones, self.instrucciones)
        grafica.genera_operaciones()
