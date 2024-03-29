from modules.Abstract.token import Token, TipoToken
import graphviz


class Graph:
    def __init__(self, datos, instrucciones):
        self.nombre = (
            datos[TipoToken.PALABRA_CLAVE_TEXT]
            if datos[TipoToken.PALABRA_CLAVE_TEXT]
            else "grafica"
        )
        self.fondo = (
            datos[TipoToken.PALABRA_CLAVE_FONDO]
            if datos[TipoToken.PALABRA_CLAVE_FONDO]
            else "#ffffff"
        )
        self.fuente = (
            datos[TipoToken.PALABRA_CLAVE_FUENTE]
            if datos[TipoToken.PALABRA_CLAVE_FUENTE]
            else "#000000"
        )
        self.forma = (
            datos[TipoToken.PALABRA_CLAVE_FORMA]
            if datos[TipoToken.PALABRA_CLAVE_FORMA]
            else "circle"
        )
        self.cambiar_forma()
        self.dot = graphviz.Digraph(
            f"{self.nombre}",
            filename=f"{self.nombre}.gv",
            node_attr={
                "shape": f"{self.forma}",
                "fontname": "Verdana",
                "fillcolor": f"{self.fondo}",
                "style": "filled",
                "fontcolor": f"{self.fuente}",
                "rankdir": "TB",
            },
            format="svg",
        )
        self.dot.attr(label=f"{self.nombre}", labelloc="t", labeljust="c")
        self.i = 0
        self.contador_n = 0
        self.ultimo = None
        self.instrucciones = instrucciones

    def cambiar_forma(self):
        if self.forma == "mdiamond":
            self.forma = "Mdiamond"
        elif self.forma == "msquare":
            self.forma = "Msquare"
        elif self.forma == "mcircle":
            self.forma = "Mcircle"

    def genera_operaciones(self):
        for ins in self.instrucciones:
            with self.dot.subgraph(name=f"cluster_{self.i}") as c:
                c.attr(label="", labelloc="t", labeljust="c")
                # print(ins)
                c.attr(color="#ffffff")
                self.contador_n = 0
                self.crear_nodos(0, c, ins)
                self.i += 1
        self.dot.format = "svg"
        self.dot.render(f"resultados/{self.nombre}", view=True)

    def crear_nodos(self, i, c, ins, anterior=None):
        ind = 0
        while ins:
            if ind >= len(ins):
                return None
            valor = ins[ind]
            if ind == 0:
                c.node(f"{self.i}_{i}_{self.contador_n}", label=f"{valor}")
                cabeza = f"{self.i}_{i}_{self.contador_n}"
                if anterior:
                    c.edge(anterior, f"{self.i}_{i}_{self.contador_n}")
                if not anterior and self.ultimo:
                    self.dot.edge(self.ultimo, cabeza, style="invis")
                    self.ultimo = None
                self.contador_n += 1
            elif valor == "[":
                ins = self.crear_nodos(i + 1, c, ins[ind + 1 :], cabeza)
                ind = 0
            elif isinstance(valor, (int, float)):
                c.node(f"{self.i}_{i}_{self.contador_n}", label=f"{valor}")
                c.edge(cabeza, f"{self.i}_{i}_{self.contador_n}")
                if not self.ultimo:
                    self.ultimo = f"{self.i}_{i}_{self.contador_n}"
                if int(self.ultimo.split("_")[1]) < i:
                    self.ultimo = f"{self.i}_{i}_{self.contador_n}"
                self.contador_n += 1
            elif valor in ["]"]:
                return ins[ind:]
            ind += 1
        return None
