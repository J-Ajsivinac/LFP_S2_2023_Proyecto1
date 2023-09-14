from modules.Abstract.token import Token, TipoToken
import math
import graphviz
import copy


class Instrucciones:
    def __init__(self, tokens, nombre):
        self.tokens = tokens
        self.instrucciones = []
        self.nombre = nombre
        self.dot = graphviz.Digraph(
            f"{nombre}",
            filename=f"{nombre}.gv",
            node_attr={
                "shape": "box",
                "fontname": "Verdana",
                "fillcolor": "#ffffff",
                "color": "#cec9f1",
                "style": "filled,rounded",
            },
            format="svg",
        )
        self.i = 0
        self.temp = []

    def operar(self, indice=0, anterior=None):
        valores = []
        op = None
        cabeza = ""
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
                cabeza = f"{op.valor}_{self.i}_{ind}"
                break
        while self.tokens:
            lexema = self.tokens.pop(0)
            if lexema.tipo == TipoToken.STRING:
                if self.tokens[0].tipo == TipoToken.STRING:
                    continue
                valor = self.tokens.pop(0)
                if valor.tipo in [TipoToken.O_OPERACION, TipoToken.LLAVE_DER]:
                    break
                if valor.tipo == TipoToken.LLAVE_IZQ:
                    valores.append(self.operar(ind + 1, cabeza))
                else:
                    if valor.tipo == TipoToken.NUMBER:
                        valores.append(valor.valor)

            if lexema.tipo in [TipoToken.O_OPERACION, TipoToken.LLAVE_DER]:
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
            result = valores[0]
            for valor in valores[1:]:
                result /= valor
            regresar = result
        elif op.tipo == TipoToken.O_POTENCIA:
            regresar = math.pow(valores[0], valores[1])
        elif op.tipo == TipoToken.O_SENO:
            regresar = math.sin(math.radians(valores[0]))
        else:
            print(f"Operación no soportada: {op}")
        valores.reverse()
        self.temp.extend(valores)
        # self.temp.append(regresar)
        self.temp.append([op, regresar])

        return regresar

    def iniciar(self):
        operacion = ""
        while True:
            operacion = self.operar()
            if operacion is not None:
                self.instrucciones.append(copy.deepcopy(self.temp))
                # self.i += 1
            else:
                break
            self.temp.clear()
        self.genera_operaciones()

    def crear_grafo(self):
        pass

    def genera_operaciones(self):
        # i = 0
        for ins in self.instrucciones:
            self.inicio(ins, 0)
            # i += 1
            self.i += 1
        self.dot.format = "png"
        self.dot.render("resultados/arbol", view=True)

    def inicio(self, ins, i, i_anterior=None, reversa=True):
        j = 0
        activar = False
        indice = None
        temp = None
        ind = 0
        if reversa:
            ins.reverse()
        for valor in ins:
            if len(ins) == 0:
                break
            if isinstance(valor, list):
                if j == 0:
                    # operacion = valor[0].valor
                    # resultado = valor[1]
                    self.dot.node(
                        f"{self.i}_{i}_{j}", label=f"{valor[0].valor}\n{valor[1]}"
                    )
                    indice = f"{self.i}_{i}_{j}"
                    if i_anterior:
                        self.dot.edge(i_anterior, indice)
                    j += 1
                else:
                    if temp != valor[1] and temp:
                        self.dot.node(f"{self.i}_{i}_{j}", label=f"{valor[1]}")
                        self.dot.edge(indice, f"{self.i}_{i}_{j}")
                        j += 1
                    else:
                        if temp:
                            # temp = j + 1
                            reg = self.inicio(ins[ind:], i + 1, indice, False)
                            if reg:
                                break
            else:
                temp = valor
                if ind < len(ins) and indice:
                    if (ind + 1) == len(ins):
                        self.dot.node(f"{self.i}_{i}_{j}", label=f"{valor}")
                        self.dot.edge(indice, f"{self.i}_{i}_{j}")
                        return True
                    elif not isinstance(ins[ind + 1], list):
                        # print(type(ins[ind + 1]))
                        self.dot.node(f"{self.i}_{i}_{j}", label=f"{valor}")
                        self.dot.edge(indice, f"{self.i}_{i}_{j}")
            j += 1
            ind += 1
        return False

    # def ramas(self, i_anterior, ins):
    #     for valor in ins:
    #         indice = None
    #         # resultado = None
    #         temp = None
    #         if isinstance(valor, list):
    #             if i == 0:
    #                 # operacion = valor[0].valor
    #                 # resultado = valor[1]
    #                 self.dot.node(f"{i}_{j}", label=f"{valor[0].valor}\n{valor[1]}")
    #                 indice = f"{i}_{j}"
    #             else:
    #                 if temp != valor[1]:
    #                     self.dot.node(indice, label=f"{valor[1]}")
    #                 else:
    #                     self.ramas(indice)
    #         else:
    #             temp = valor
