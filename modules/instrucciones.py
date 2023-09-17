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

    def operar(self, indice=0, recursivo=False):
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
                        self.temp.append(valor.valor)
                        valores.append(valor.valor)

            if lexema.tipo in [TipoToken.LLAVE_DER, TipoToken.CORCHETE_DER]:
                self.temp.append(lexema.valor)
            if lexema.tipo in [TipoToken.O_OPERACION, TipoToken.CORCHETE_IZQ]:
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
            result = valores[0] / valores[1]
            regresar = result
        elif op.tipo == TipoToken.O_POTENCIA:
            regresar = math.pow(valores[0], valores[1])
        elif op.tipo == TipoToken.O_RAIZ:
            regresar = math.pow(valores[0], 0.5)
        elif op.tipo == TipoToken.O_SENO:
            regresar = math.sin(math.radians(valores[0]))
        elif op.tipo == TipoToken.O_COSENO:
            regresar = math.cos(math.radians(valores[0]))
        elif op.tipo == TipoToken.O_TANGENTE:
            regresar = math.tan(math.radians(valores[0]))
        elif op.tipo == TipoToken.O_MOD:
            regresar = valor[0] % valor[1]
        else:
            print(f"Operación no soportada: {op}")
        valores.reverse()

        self.temp[iterador] += str(regresar)
        # self.temp.append(regresar)

        # self.temp.append(regresar)
        # self.temp.append(op.valor + "\n" + str(regresar))
        # for i, valor in enumerate(valores):
        #     self.temp[f"valor{ind}_{i}"] = valor
        # self.temp[f"operacion_{ind}"] = op.valor + " " + str(regresar)
        return regresar

    def iniciar(self):
        operacion = ""
        while True:
            operacion = self.operar()
            if operacion is not None:
                # self.temp.reverse()
                # self.temp.reverse()
                self.instrucciones.append(copy.deepcopy(self.temp))
                # self.i += 1
            else:
                break
            self.temp.clear()
        # for i in self.instrucciones:
        #     print(i, "------")
        self.genera_operaciones()

    def crear_grafo(self):
        pass

    def genera_operaciones(self):
        for ins in self.instrucciones:
            self.crear_nodos(0, ins)
            # print(ins)
            self.i += 1
        self.dot.format = "svg"
        self.dot.render("resultados/arbol1", view=True)

    def crear_nodos(self, i, ins, anterior=None):
        j = 0
        ind = 0
        while ins:
            if ind >= len(ins):
                return None
            valor = ins[ind]
            if j == 0:
                self.dot.node(f"{self.i}_{i}_{j}", label=f"{valor}")
                cabeza = f"{self.i}_{i}_{j}"
                if anterior:
                    self.dot.edge(anterior, f"{self.i}_{i}_{j}")
                    # print(valor, anterior, f"{self.i}_{i}_{j}")
                j += 1

            elif valor == "[":
                ins = self.crear_nodos(i + 1, ins[ind + 1 :], cabeza)
                ind = 0
                # print(f"---{cabeza}---")
            elif isinstance(valor, (int, float)):
                self.dot.node(f"{self.i}_{i}_{j}", label=f"{valor}")
                # print(f"{valor}")
                self.dot.edge(cabeza, f"{self.i}_{i}_{j}")
                j += 1
            elif valor in ["]", "{"]:
                return ins[ind:]
            ind += 1
        return None
