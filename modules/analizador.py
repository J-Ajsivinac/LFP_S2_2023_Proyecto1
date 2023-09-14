from modules.Abstract.token import Token, TipoToken
from modules.Abstract.error import Error
import re
import math


class Analizador:
    def __init__(self):
        self.tokens = []
        self.errores = []
        self.estado = 0
        self.fila = 1
        self.columna = 0
        self.instrucciones = []
        self.esoperacion = False
        self.operaciones_switch = True
        self.abierto = False
        self.patterns = [
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
        ]

    def s_0(self, caracter, cadena):
        if caracter == "{":
            self.estado = 1
            self.columna += 1
        elif caracter == ":":
            self.estado = 2
            self.columna += 1
        elif caracter == "[":
            self.estado = 3
            self.columna += 1
        elif caracter == '"':
            self.estado = 4
            self.columna += 1
        elif caracter == "]":
            self.estado = 6
            self.columna += 1
        elif caracter == ",":
            self.estado = 7
            self.columna += 1
        elif caracter == "}":
            self.estado = 8
            self.columna += 1
        elif not self.abierto and caracter.isalpha():
            self.crear_error('se esperaba un " ', self.fila, self.columna)
            cadena = self.s_5(cadena, 0)
        else:
            self.crear_error(caracter, self.fila, self.columna)
            self.columna += 1
            cadena = cadena[1:]
            if self.esoperacion:
                self.esoperacion = False
        return cadena

    def s_1(self):
        self.tokens.append(Token(TipoToken.LLAVE_IZQ, "{", self.fila, self.columna))
        self.estado = 0

    def s_2(self):
        self.tokens.append(Token(TipoToken.DOS_PUNTOS, ":", self.fila, self.columna))
        self.estado = 0

    def s_3(self):
        self.tokens.append(Token(TipoToken.CORCHETE_IZQ, "[", self.fila, self.columna))
        self.estado = 0

    def s_4(self):
        self.tokens.append(Token(TipoToken.COMILLA, '"', self.fila, self.columna))
        self.estado = 0
        self.abierto = False if self.abierto else True

    def s_5(self, cadena, puntero):
        estado, cadena, puntero = self.crear_objeto(cadena, puntero, not self.abierto)
        if estado:
            self.estado = estado
        else:
            self.estado = 9
        return cadena

    def s_6(self):
        self.tokens.append(Token(TipoToken.LLAVE_DER, "]", self.fila, self.columna))
        self.estado = 0

    def s_7(self):
        self.tokens.append(Token(TipoToken.COMA, ",", self.fila, self.columna))
        self.estado = 0

    def s_8(self):
        self.tokens.append(Token(TipoToken.LLAVE_DER, "}", self.fila, self.columna))
        self.estado = 0

    def s_9(self, cadena, puntero):
        cadena, puntero = self.dos_valores(cadena, puntero)
        return cadena

    def leer_instrucciones(self, cadena):
        puntero = 0
        self.estado = 0

        while cadena:
            char = cadena[puntero]
            if char == "\t":
                self.columna += 4
                cadena = cadena[4:]
                puntero = 0
                continue
            if char == "\n":
                self.columna = 0
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
                cadena = self.s_0(cadena[puntero], cadena)
            elif self.estado == 1:
                self.s_1()
                cadena = cadena[1:]
                puntero = 0
            elif self.estado == 2:
                self.s_2()
                cadena = cadena[1:]
                puntero = 0
            elif self.estado == 3:
                self.s_3()
                cadena = cadena[1:]
                puntero = 0
                cadena = self.leer_instrucciones(cadena)
            elif self.estado == 4:
                self.s_4()
                cadena = cadena[1:]
                puntero = 0
                cadena = self.s_5(cadena, puntero)
            elif self.estado == 6:
                self.s_6()
                cadena = cadena[1:]
                puntero = 0
                break
            elif self.estado == 7:
                self.s_7()
                cadena = cadena[1:]
                puntero = 0
            elif self.estado == 8:
                self.s_8()
                cadena = cadena[1:]
                puntero = 0
                # self.estado = 0
            elif self.estado == 9:
                # _, cadena, puntero = self.crear_objeto(cadena, puntero)
                if char == ",":
                    self.columna += 1
                    self.tokens.append(
                        Token(TipoToken.COMA, ",", self.fila, self.columna)
                    )
                    cadena = cadena[1:]
                    puntero = 0
                    self.estado = 11
                else:
                    self.estado = 0
                    puntero = 0
            elif self.estado == 11:
                cadena = self.s_9(cadena, puntero)
                puntero = 0
                self.estado = 0

            # self.i += 1
            # puntero += 1
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
        self.errores.append(
            Error(len(self.errores) + 1, "Error Léxico", fila, columna, lexema)
        )

    def crear_objeto(self, cadena, puntero, es_error=False):
        estado, token_type, lexema, cadena = self.crear_lexema(cadena[puntero:])
        puntero = 0
        if lexema and cadena:
            self.columna += 1
            if not es_error:
                es_error = True if token_type is None else False
            if not es_error:
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

            if char == "," or char == ":":
                cadena = cadena[puntero:]
                puntero = 0
                continue
            if char == "}":
                puntero = 0
                break

            if estado == 0:
                contador += 1
                if char == "[":
                    self.tokens.append(
                        Token(TipoToken.LLAVE_IZQ, "[", self.fila, self.columna)
                    )
                    cadena = cadena[1:]
                    puntero = 0
                    self.columna += 1
                    cadena = self.leer_instrucciones(cadena)

                es_numero = True if (contador % 2) == 0 else False
                if char == '"':
                    if not es_numero:
                        _, cadena, puntero = self.crear_objeto(cadena, puntero)
                    elif not self.operaciones_switch:
                        _, cadena, puntero = self.crear_objeto(cadena, puntero)
                    else:
                        self.crear_error(
                            "Se esperaba un Número", self.fila, self.columna + 1
                        )
                        _, cadena, puntero = self.crear_objeto(cadena, puntero, True)
                    # self.estado = estado
                elif (
                    ord(char) == 43
                    or ord(char) == 45
                    or (ord(char) >= 48 and ord(char) <= 57)
                ):
                    lexema, cadena, es_error = self.crear_numero(cadena)
                    if lexema and cadena:
                        self.columna += 1
                        if not es_error:
                            lex = Token(
                                TipoToken.NUMBER, lexema, self.fila, self.columna
                            )
                            self.tokens.append(lex)
                        self.columna += len(str(lexema)) + 1
                        puntero = 0
                elif char != "[":
                    self.limpiar(cadena)
                    self.columna += 1
                    cadena = cadena[1:]
                    puntero = 0
                    self.crear_error(char, self.fila, self.columna)

                # if (contador % 2) == 0:
                #     estado = 1
                # else:
                #     estado = 2

        return cadena, puntero

    def crear_numero(self, cadena):
        numero = ""
        puntero = 0
        es_decimal = False
        es_error = False
        for char in cadena:
            puntero += 1
            if char == ".":
                es_decimal = True

            if (
                char == '"'
                or char == "\n"
                or char == "\t"
                or char == ","
                or (not char.isdigit() and char != ".")
            ):
                if es_decimal:
                    return float(numero), cadena[puntero - 1 :], es_error
                return int(numero), cadena[puntero - 1 :], es_error
            else:
                if es_decimal:
                    if char == "." and "." in numero:
                        self.crear_error(
                            "no se pueden tener más de dos .",
                            self.fila,
                            self.columna + len(numero),
                        )
                        es_error = True
                    else:
                        numero += char
                else:
                    numero += char

    def imprimir(self):
        for lexema in self.tokens:
            print(f"{lexema.valor}---{lexema.columna}")
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
                or char == ","
            ):
                if char == ":":
                    puntero -= 1

                if char != '"' and self.abierto:
                    self.crear_error(
                        'se esperaba un "', self.fila, self.columna + len(lexema)
                    )
                token_type = None
                for pattern, pattern_type in self.patterns:
                    if re.fullmatch(pattern, lexema):
                        token_type = pattern_type
                        break
                if token_type in [TipoToken.O_OPERACION]:
                    self.esoperacion = True
                    return None, token_type, lexema, cadena[puntero:]

                if token_type in [TipoToken.CONFIGURACIONES, TipoToken.PALABRA_CLAVE]:
                    self.operaciones_switch = False

                if self.esoperacion:
                    if token_type:
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
                            return 9, token_type, lexema, cadena[puntero:]
                        else:
                            self.crear_error(lexema, self.fila, self.columna)
                            self.esoperacion = False
                            return 9, None, lexema, cadena[puntero:]
                    else:
                        self.crear_error(lexema, self.fila, self.columna)
                        self.esoperacion = False
                        return 9, None, lexema, cadena[puntero:]
                else:
                    if isinstance(lexema, str):
                        return 0, TipoToken.STRING, lexema, cadena[puntero:]
                    else:
                        return 0, token_type, lexema, cadena[puntero:]
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


# text = ""
# with open(
#     "C:\\Users\\mesoi\\Documents\\1U^NI6VxExD@D\\2023\\2. SEGUNDO SEMESTRE\\LFP\\Lab\\Proyecto 1\\entrada.json",
#     "r",
# ) as json_file:
#     text = json_file.read()
# analizado = Analizador()
# analizado.leer_instrucciones(text)
# analizado.imprimir()
# analizado.iniciar()
