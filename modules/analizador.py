from modules.Abstract.token import Token, TipoToken
import re
import math


class Analizador:
    def __init__(self):
        self.tokens = []
        self.errores = {"errores": []}
        self.estado = 0
        self.fila = 1
        self.columna = 1
        self.instrucciones = []
        self.esoperacion = False
        self.patterns = [
            (r"\d+\.\d+", TipoToken.NUMBER),  # Número decimal
            (
                re.compile(
                    r"operaciones",
                    re.I,
                ),
                TipoToken.OPERACIONES,
            ),
            (
                re.compile(
                    r"configuraciones",
                    re.I,
                ),
                TipoToken.CONFIGURACIONES,
            ),
            (
                re.compile(
                    r"operacion",
                    re.I,
                ),
                TipoToken.O_OPERACION,
            ),
            (
                re.compile(
                    r"(text|fondo|azul|fuente|forma|circulo)",
                    re.I,
                ),
                TipoToken.PALABRA_CLAVE,
            ),
            (
                re.compile(
                    r"(suma)",
                    re.I,
                ),
                TipoToken.O_SUMA,
            ),
            (
                re.compile(
                    r"(resta)",
                    re.I,
                ),
                TipoToken.O_RESTA,
            ),
            (
                re.compile(
                    r"(multiplicacion)",
                    re.I,
                ),
                TipoToken.O_MULTIPLICACION,
            ),
            (
                re.compile(
                    r"(division)",
                    re.I,
                ),
                TipoToken.O_DIVISION,
            ),
            (
                re.compile(
                    r"(potencia)",
                    re.I,
                ),
                TipoToken.O_POTENCIA,
            ),
            (
                re.compile(
                    r"(seno)",
                    re.I,
                ),
                TipoToken.O_SENO,
            ),
            (r"[{}:\[\],]", "SIMBOLO_ESPECIAL"),  # Símbolos especiales
            (r"\s+", "ESPACIO"),
            (r"^[a-zA-Z_][a-zA-Z0-9_]*$", TipoToken.STRING),  # Espacios en blanco
        ]

    def leer_instrucciones(self, cadena, coma=False):
        puntero = 0
        self.estado = 0

        while cadena:
            char = cadena[puntero]
            puntero += 1
            if char == "\t":
                self.columna += 4
                cadena = cadena[4:]
                puntero = 0
                continue
            if char == "\n":
                self.columna = 1
                self.fila += 1
                cadena = cadena[1:]
                puntero = 0
                continue
            if char == " ":
                cadena = cadena[1:]
                puntero = 0
                self.columna += 1
                continue

            if self.estado == 0:
                if char == "{":
                    cadena = cadena[1:]
                    puntero = 0
                    self.columna += 1
                else:
                    # print("se esperaba un {")
                    self.crear_error("Se esperaba un {", self.fila, self.columna)
                    puntero = 0
                self.estado = 1

            elif self.estado == 1:
                if char == "}":
                    break
                if char == '"':
                    _, cadena, puntero = self.crear_objeto(cadena, puntero)
                elif char.isalpha():
                    self.crear_error('Se esperaba un "', self.fila, self.columna)
                    _, cadena, puntero = self.crear_objeto(cadena, puntero - 1, True)
                else:
                    self.columna = 1
                    cadena = cadena[1:]
                    puntero = 0
                    self.crear_error(f"{char}", self.fila, self.columna)
                    puntero = 0
                    self.estado = 1
                    continue
                self.estado = 2
            elif self.estado == 2:
                puntero, cadena = self.verificar_caracter(char, puntero, ":", cadena)
                self.estado = 3
            elif self.estado == 3:
                # estado de arreglos
                if char == "[":
                    self.tokens.append(
                        Token(TipoToken.LLAVE_IZQ, "[", self.fila, self.columna)
                    )
                    cadena = cadena[1:]
                    puntero = 0
                    self.columna += 1
                    if len(self.tokens) == 2:
                        cadena = self.leer_instrucciones(cadena, True)
                    else:
                        cadena = self.leer_instrucciones(cadena)
                # estado de palabras reservadas
                if char == '"':
                    estado, cadena, puntero = self.crear_objeto(cadena, puntero)
                    if estado:
                        self.estado = estado
                    else:
                        self.estado = 5
                elif char == "{":
                    self.crear_error("Se esperaba un [", self.fila, self.columna)
                    cadena = self.leer_instrucciones(cadena, True)

            elif self.estado == 4:
                puntero, cadena = self.verificar_caracter(char, puntero, ",", cadena)
                cadena, puntero = self.un_valor(cadena, puntero)
                self.estado = 6
            elif self.estado == 5:
                puntero, cadena = self.verificar_caracter(char, puntero, ",", cadena)
                cadena, puntero = self.dos_valores(cadena, puntero)
                self.estado = 6
            elif self.estado == 6:
                if char != "}":
                    # print("se esperaba un }")
                    self.crear_error("Se esperaba un }", self.fila, self.columna)
                    puntero = 0
                if char == "}":
                    cadena = cadena[1:]
                    puntero = 0
                    self.columna += 1
                self.estado = 7
            elif self.estado in [7, 10]:
                if char == ",":
                    cadena = cadena[1:]
                    puntero = 0
                    self.columna += 1
                    cadena, puntero = self.limpiar(cadena)
                    puntero = 0
                    if cadena[puntero] == '"' or self.estado == 10:
                        puntero = 0
                        break
                    cadena = self.leer_instrucciones(cadena)
                elif char == "]":
                    self.tokens.append(
                        Token(TipoToken.LLAVE_DER, "]", self.fila, self.columna)
                    )
                    cadena = cadena[1:]
                    puntero = 0
                    self.columna += 1
                    if coma:
                        break
                    self.estado = 8
                    continue
                else:
                    self.crear_error("Se esperaba un ,", self.fila, self.columna)
                    puntero = 0
                self.estado = 1
            elif self.estado == 8:
                if char == ",":
                    puntero = 0
                    if coma:
                        break
                elif char == "}":
                    cadena = cadena[1:]
                    puntero = 0
                    self.columna += 1
                elif char == "]":
                    if coma:
                        break
                elif char != "}" or char != "]":
                    # print("se esperaba un }")
                    # self.crear_error("Se esperaba un },] ','", self.fila, self.columna)
                    puntero = 0
                self.estado = 7
        return cadena

    def limpiar(self, cadena):
        puntero = 0
        while cadena and (puntero < len(cadena) - 1):
            char = cadena[puntero]
            puntero += 1
            if char == "\t":
                self.columna += 4
                cadena = cadena[4:]
                puntero = 0
                continue
            if char == "\n":
                self.columna = 1
                self.fila += 1
                cadena = cadena[1:]
                puntero = 0
                continue
            if char == " ":
                cadena = cadena[1:]
                puntero = 0
                self.columna += 1
                continue
            else:
                break
        return cadena, puntero

    def verificar_caracter(self, char, puntero, comparacion, cadena):
        if char == comparacion:
            cadena = cadena[1:]
            puntero = 0
            self.columna += 1
        else:
            # print(f"se esperaba un {comparacion}")
            puntero = 0
            self.crear_error(f"Se esperaba un {comparacion}", self.fila, self.columna)
        return puntero, cadena

    def crear_error(self, lexema, fila, columna):
        nuevo_error = {
            "No": len(self.errores["errores"]) + 1,
            "descripcion": {
                "lexema": lexema,
                "tipo": "Error",
                "columna": columna,
                "fila": fila,
            },
        }
        self.errores["errores"].append(nuevo_error)

    def crear_objeto(self, cadena, puntero, eserror=False):
        estado, token_type, lexema, cadena = self.crear_lexema(cadena[puntero:])
        puntero = 0
        if lexema and cadena:
            self.columna += 1
            if not eserror:
                lex = Token(token_type, lexema, self.fila, self.columna)
                self.tokens.append(lex)
            # estado = 7
            self.columna += len(str(lexema)) + 1
            puntero = 0
        return estado, cadena, puntero

    def dos_valores(self, cadena, puntero):
        estado = 0
        contador = 0
        puntero = 0
        while cadena:
            char = cadena[puntero]
            puntero += 1
            if char == "\t":
                self.columna += 4
                cadena = cadena[4:]
                puntero = 0
                continue
            if char == "\n":
                self.columna = 1
                self.fila += 1
                cadena = cadena[1:]
                puntero = 0
                continue
            if char == " ":
                cadena = cadena[1:]
                puntero = 0
                self.columna += 1
                continue

            if estado == 0:
                if char == "[":
                    self.tokens.append(
                        Token(TipoToken.LLAVE_IZQ, "[", self.fila, self.columna)
                    )
                    cadena = cadena[1:]
                    puntero = 0
                    self.columna += 1
                    if (contador % 2) == 0:
                        # if contador == 2:
                        cadena = self.leer_instrucciones(cadena)
                    else:
                        cadena = self.leer_instrucciones(cadena, True)
                # estado de palabras reservadas
                if char == '"':
                    _, cadena, puntero = self.crear_objeto(cadena, puntero)
                    # self.estado = estado
                elif (
                    ord(char) == 43
                    or ord(char) == 45
                    or (ord(char) >= 48 and ord(char) <= 57)
                ):
                    lexema, cadena = self.crear_numero(cadena)
                    if lexema and cadena:
                        self.columna += 1
                        lex = Token(TipoToken.NUMBER, lexema, self.fila, self.columna)
                        self.tokens.append(lex)
                        self.columna += len(str(lexema)) + 1
                        puntero = 0
                elif char != "[":
                    self.limpiar(cadena)
                    self.columna += 1
                    cadena = cadena[1:]
                    puntero = 0
                    self.crear_error(char, self.fila, self.columna)

                if (contador % 2) == 0:
                    estado = 1
                else:
                    estado = 2
            elif estado == 1:
                puntero, cadena = self.verificar_caracter(char, puntero, ":", cadena)
                contador += 1
                estado = 0
            elif estado == 2:
                if char == "}":
                    puntero = 0
                    break
                contador += 1
                puntero, cadena = self.verificar_caracter(char, puntero, ",", cadena)
                estado = 0

        return cadena, puntero

    def crear_numero(self, cadena):
        numero = ""
        puntero = 0
        es_decimal = False
        for char in cadena:
            puntero += 1
            if char == ".":
                es_decimal = True
            if (
                char == '"'
                or char == " "
                or char == "\n"
                or char == "\t"
                or char == ","
            ):
                if es_decimal:
                    return float(numero), cadena[puntero - 1 :]
                else:
                    return int(numero), cadena[puntero - 1 :]
            else:
                numero += char

    def imprimir(self):
        for lexema in self.tokens:
            print(f"{lexema.valor}-{lexema.tipo}")
        for error in self.errores["errores"]:
            print(error)

    def crear_lexema(self, cadena):
        lexema = ""
        puntero = 0

        for char in cadena:
            puntero += 1
            if (
                char == '"'
                or char == " "
                or char == "\n"
                or char == "\t"
                or char == ":"
            ):
                if char == ":":
                    puntero -= 1

                if char != '"':
                    self.crear_error(
                        'se esperaba un "', self.fila, self.columna + len(lexema) + 1
                    )
                token_type = None
                for pattern, pattern_type in self.patterns:
                    if re.fullmatch(pattern, lexema):
                        token_type = pattern_type
                        break
                if token_type:
                    if token_type in [TipoToken.O_OPERACION]:
                        self.esoperacion = True
                        return None, token_type, lexema, cadena[puntero:]
                    if self.esoperacion:
                        if token_type in [
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
                            TipoToken.O_OPERACION,
                        ]:
                            self.esoperacion = False
                            return 5, token_type, lexema, cadena[puntero:]
                        else:
                            self.crear_error(lexema, self.fila, self.columna)
                            self.esoperacion = False
                            break
                    else:
                        if token_type in [TipoToken.STRING]:
                            return 5, token_type, lexema, cadena[puntero:]
                        else:
                            return None, token_type, lexema, cadena[puntero:]
                else:
                    self.crear_error(lexema, self.fila, self.columna)
                    break
            else:
                lexema += char
        return None, None, None, cadena[puntero:]

    def operar(self):
        valores = []
        op = None
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

        while self.tokens:
            lexema = self.tokens.pop(0)
            if lexema.tipo == TipoToken.STRING:
                if self.tokens[0].tipo == TipoToken.STRING:
                    continue
                valor = self.tokens.pop(0)
                if valor.tipo in [TipoToken.O_OPERACION, TipoToken.LLAVE_DER]:
                    break
                if valor.tipo == TipoToken.LLAVE_IZQ:
                    valores.append(self.operar())
                else:
                    if valor.tipo == TipoToken.NUMBER:
                        valores.append(valor.valor)

            if lexema.tipo in [TipoToken.O_OPERACION, TipoToken.LLAVE_DER]:
                break
        if len(valores) == 0 and len(self.tokens) == 0 and not op:
            return None

        if op.tipo == TipoToken.O_SUMA:
            return sum(valores)
        elif op.tipo == TipoToken.O_RESTA:
            return valores[0] - sum(valores[1:])
        elif op.tipo == TipoToken.O_MULTIPLICACION:
            result = 1
            for valor in valores:
                result *= valor
            return result
        elif op.tipo == TipoToken.O_DIVISION:
            result = valores[0]
            for valor in valores[1:]:
                result /= valor
            return result
        elif op.tipo == TipoToken.O_POTENCIA:
            return math.pow(valores[0], valores[1])
        elif op.tipo == TipoToken.O_SENO:
            return math.sin(valores[0])
        else:
            print(f"Operación no soportada: {op}")
        return None

    def iniciar(self):
        operacion = ""
        while True:
            operacion = self.operar()
            if operacion is not None:
                self.instrucciones.append(operacion)
            else:
                break

        for i in self.instrucciones:
            print(i)


# analizado = Analizador()
# analizado.leer_instrucciones(text)
# analizado.imprimir()
# analizado.iniciar()
