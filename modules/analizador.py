from Abstract.token import Token, TipoToken
import re


class Analizador:
    def __init__(self):
        self.tokens = []
        self.errores = []
        self.estado = 0
        self.fila = 1
        self.columna = 1
        self.instrucciones = []
        self.patterns = [
            (r"\d+\.\d+", "NUMERO"),  # Número decimal
            (
                re.compile(
                    r"operacion",
                    re.I,
                ),
                TipoToken.O_OPERACION,
            ),
            (
                re.compile(
                    r"(operaciones|configuraciones|text|fondo|azul|fuente|forma|circulo)",
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
                    print("se esperaba un {")
                self.estado = 1

            elif self.estado == 1:
                if char == '"':
                    _, cadena, puntero = self.crear_crear_objeto(cadena, puntero)

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
                    estado, cadena, puntero = self.crear_crear_objeto(cadena, puntero)
                    if estado:
                        self.estado = estado
            elif self.estado == 4:
                puntero, cadena = self.verificar_caracter(char, puntero, ",", cadena)
                cadena, puntero = self.un_valor(cadena, puntero)
                self.estado = 6
            elif self.estado == 5:
                puntero, cadena = self.verificar_caracter(char, puntero, ",", cadena)
                cadena, puntero = self.dos_valores(cadena, puntero)
                if coma:
                    if char == "]":
                        self.estado = 7
                self.estado = 6
            elif self.estado == 6:
                if char != "}":
                    print("se esperaba un }")
                if char == "}":
                    cadena = cadena[1:]
                    puntero = 0
                    self.columna += 1
                self.estado = 7
            elif self.estado == 7:
                if char == ",":
                    cadena = cadena[1:]
                    puntero = 0
                    self.columna += 1
                    cadena, puntero = self.limpiar(cadena)
                    puntero = 0
                    if cadena[puntero] == '"':
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
                    print("XD")
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
                    print("se esperaba un }")
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
            print(f"se esperaba un {comparacion}")
        return puntero, cadena

    def crear_crear_objeto(self, cadena, puntero):
        estado, token_type, lexema, cadena = self.crear_lexema(cadena[puntero:])
        if lexema and cadena:
            self.columna += 1
            lex = Token(token_type, lexema, self.fila, self.columna)
            self.tokens.append(lex)
            self.columna += len(str(lexema)) + 1
            puntero = 0
        return estado, cadena, puntero

    def dos_valores(self, cadena, puntero):
        estado = 0
        contador = 0
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
                    estado, cadena, puntero = self.crear_crear_objeto(cadena, puntero)
                    # self.estado = estado
                if (
                    ord(char) == 43
                    or ord(char) == 45
                    or (ord(char) >= 48 and ord(char) <= 57)
                ):
                    lexema, cadena = self.crear_numero(cadena)
                    if lexema and cadena:
                        self.columna += 1
                        lex = Token("NUMERO", lexema, self.fila, self.columna)
                        self.tokens.append(lex)
                        self.columna += len(str(lexema)) + 1
                        puntero = 0

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

    def un_valor(self, cadena, puntero):
        estado = 0
        contador = 0
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
                contador += 1
                if char == "[":
                    self.tokens.append(
                        Token(TipoToken.LLAVE_IZQ, "[", self.fila, self.columna)
                    )
                    cadena = cadena[1:]
                    puntero = 0
                    self.columna += 1
                    if contador == 2:
                        cadena = self.leer_instrucciones(cadena, True)
                    else:
                        cadena = self.leer_instrucciones(cadena)
                # estado de palabras reservadas
                if char == '"':
                    estado, cadena, puntero = self.crear_crear_objeto(cadena, puntero)
                    # self.estado = estado
                if (
                    ord(char) == 43
                    or ord(char) == 45
                    or (ord(char) >= 48 and ord(char) <= 57)
                ):
                    lexema, cadena = self.crear_numero(cadena)
                    if lexema and cadena:
                        self.columna += 1
                        lex = Token("NUMERO", lexema, self.fila, self.columna)
                        self.tokens.append(lex)
                        self.columna += len(str(lexema)) + 1
                        puntero = 0

                if contador == 1:
                    estado = 1
                elif contador == 2:
                    estado = 3
                elif contador == 3:
                    estado = 3

            elif estado == 1:
                puntero, cadena = self.verificar_caracter(char, puntero, ":", cadena)
                estado = 0
            elif estado == 3:
                puntero = 0
                break
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

    def crear_lexema(self, cadena):
        lexema = ""
        puntero = 0

        for char in cadena:
            puntero += 1
            if char == '"':
                token_type = None
                for pattern, pattern_type in self.patterns:
                    if re.fullmatch(pattern, lexema):
                        token_type = pattern_type
                        break
                if token_type:
                    if token_type in [
                        TipoToken.O_INVERSO,
                        TipoToken.O_SENO,
                        TipoToken.O_COSENO,
                        TipoToken.O_TANGENTE,
                    ]:
                        return 4, token_type, lexema, cadena[puntero:]
                    elif token_type in [
                        TipoToken.O_SUMA,
                        TipoToken.O_RESTA,
                        TipoToken.O_MULTIPLICACION,
                        TipoToken.O_DIVISION,
                        TipoToken.O_POTENCIA,
                        TipoToken.O_RAIZ,
                        TipoToken.O_MOD,
                        TipoToken.STRING,
                    ]:
                        return 5, token_type, lexema, cadena[puntero:]
                    return None, token_type, lexema, cadena[puntero:]
                else:
                    print(f"Token no válido: {lexema}")
                    break
            else:
                lexema += char
        return None, None, None, cadena[puntero:]


text = ""
with open(
    "C:\\Users\\mesoi\\Documents\\1U^NI6VxExD@D\\2023\\2. SEGUNDO SEMESTRE\\LFP\\Lab\\Proyecto 1\\entrada.json",
    "r",
) as json_file:
    text = json_file.read()

analizado = Analizador()
analizado.leer_instrucciones(text)
# analizado.imprimir()
# analizado.iniciar()
