from modules.Abstract.error import Error
from modules.Abstract.token import Token, TipoToken
import re


class Analizador:
    def __init__(self):
        self.tokens = []
        self.errores = []
        self.estado = 0
        self.fila = 1
        self.columna = 0
        self.instrucciones = []
        self.abierto = False
        self.patterns = [
            ("operaciones", TipoToken.OPERACIONES),
            ("configuraciones", TipoToken.CONFIGURACIONES),
            ("operacion", TipoToken.O_OPERACION),
            ("suma", TipoToken.O_SUMA),
            ("resta", TipoToken.O_RESTA),
            ("multiplicacion", TipoToken.O_MULTIPLICACION),
            ("division", TipoToken.O_DIVISION),
            ("potencia", TipoToken.O_POTENCIA),
            ("seno", TipoToken.O_SENO),
            ("coseno", TipoToken.O_COSENO),
            ("tangente", TipoToken.O_TANGENTE),
            ("texto", TipoToken.PALABRA_CLAVE_TEXT),
            ("fondo", TipoToken.PALABRA_CLAVE_FONDO),
            ("fuente", TipoToken.PALABRA_CLAVE_FUENTE),
            ("forma", TipoToken.PALABRA_CLAVE_FORMA),
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
        elif (caracter.isalpha()) and self.abierto:
            self.estado = 5
            # self.columna += 1
        elif caracter.isdigit() or ord(caracter) == 43 or ord(caracter) == 45:
            self.estado = 9
            # self.columna += 1
        elif caracter == "]":
            self.estado = 6
            self.columna += 1
        elif caracter == ",":
            self.estado = 7
            self.columna += 1
        elif caracter == "}":
            self.estado = 8
            self.columna += 1
        elif caracter == ",":
            self.columna += 1
            self.tokens.append(Token(TipoToken.COMA, ",", self.fila, self.columna))
            cadena = cadena[1:]
            self.estado = 0
        else:
            self.crear_error(caracter, self.fila, self.columna)
            self.columna += 1
            cadena = cadena[1:]
        return cadena

    def s_1(self):
        self.tokens.append(Token(TipoToken.CORCHETE_IZQ, "{", self.fila, self.columna))
        self.estado = 0

    def s_2(self):
        self.tokens.append(Token(TipoToken.DOS_PUNTOS, ":", self.fila, self.columna))
        self.estado = 0

    def s_3(self):
        self.tokens.append(Token(TipoToken.LLAVE_IZQ, "[", self.fila, self.columna))
        self.estado = 0

    def s_4(self):
        self.tokens.append(Token(TipoToken.COMILLA, '"', self.fila, self.columna))
        self.estado = 0
        self.abierto = False if self.abierto else True

    def s_5(self, cadena, puntero):
        estado, cadena, puntero = self.crear_objeto(cadena, puntero)
        if estado:
            self.estado = estado
        else:
            self.estado = 0
        return cadena

    def s_6(self):
        self.tokens.append(Token(TipoToken.LLAVE_DER, "]", self.fila, self.columna))
        self.estado = 0

    def s_7(self):
        self.tokens.append(Token(TipoToken.COMA, ",", self.fila, self.columna))
        self.estado = 0

    def s_8(self):
        self.tokens.append(Token(TipoToken.CORCHETE_DER, "}", self.fila, self.columna))
        self.estado = 0

    def s_9(self, cadena, puntero):
        cadena, puntero = self.dos_valores(cadena, puntero)
        self.estado = 0
        return cadena

    def leer_instrucciones(self, cadena):
        puntero = 0
        self.estado = 0

        while cadena:
            cadena, puntero = self.limpiar(cadena)
            if not cadena:
                break
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
                # cadena = self.s_5(cadena, puntero)
            elif self.estado == 5:
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
                cadena = self.s_9(cadena, puntero)

            elif self.estado == 11:
                cadena = self.s_9(cadena, puntero)
                puntero = 0
                self.estado = 0

            # self.i += 1
            # puntero += 1
        return cadena

    def limpiar(self, cadena):
        puntero = 0
        while cadena and (puntero <= len(cadena) - 1):
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

            puntero = 0
            break
        return cadena, puntero

    def crear_error(self, lexema, fila, columna):
        self.errores.append(
            Error(len(self.errores) + 1, "Error Léxico", fila, columna, lexema)
        )

    def crear_objeto(self, cadena, puntero, es_error=False):
        estado, token_type, lexema, cadena = self.crear_lexema(cadena[puntero:])
        puntero = 0
        if lexema and cadena:
            # if not es_error:
            #     es_error = True if token_type is None else False
            if not es_error:
                lex = Token(token_type, lexema, self.fila, self.columna)
                self.tokens.append(lex)
            # estado = 7
            self.columna += len(str(lexema))
            puntero = 0
        return estado, cadena, puntero

    def dos_valores(self, cadena, puntero):
        puntero = 0
        while cadena:
            cadena, puntero = self.limpiar(cadena)
            char = cadena[puntero]

            # self.estado = estado
            if ord(char) == 43 or ord(char) == 45 or char.isdigit():
                lexema, cadena, es_error = self.crear_numero(cadena)
                if lexema and cadena:
                    self.columna += 1
                    if not es_error:
                        lex = Token(TipoToken.NUMBER, lexema, self.fila, self.columna)
                        self.tokens.append(lex)
                    self.columna += len(str(lexema)) + 1
                    puntero = 0
                break

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
                    if char.isdigit():
                        numero += char
                    else:
                        self.crear_error(char, self.fila, self.columna)

    def crear_lexema(self, cadena):
        lexema = ""
        puntero = 0

        for char in cadena:
            puntero += 1
            if (
                char == '"'
                or char == "\n"
                or char == "\t"
                or char == ":"
                or char == ","
            ):
                if char == ":":
                    puntero -= 1

                if char == '"':
                    puntero -= 1

                token_type = None
                for pattern, pattern_type in self.patterns:
                    if pattern == lexema:
                        token_type = pattern_type
                        break

                if token_type:
                    return 0, token_type, lexema, cadena[puntero:]
                return 0, TipoToken.STRING, lexema, cadena[puntero:]
            else:
                if char.isalpha() or char.isdigit():
                    lexema += char
                else:
                    self.crear_error(char, self.fila, self.columna)
        return None, None, None, cadena[puntero:]
