<h1 align="center">Manual Técnico</h1>

<div align="center">
🙍‍♂️ Joab Israel Ajsivinac Ajsivinac 🆔 202200135
</div>
<div align="center">
📕 Lenguajes Formales y de Programación
</div>
<div align="center"> 🏛 Universidad San Carlos de Guatemala</div>
<div align="center"> 📆 Segundo Semestre 2023</div>

<!-- Tabla de Contenidos -->
## 📋 Tabla de Contenidos

<!-- - [📋 Tabla de Contenidos](#-tabla-de-contenidos) -->
- [📋 Tabla de Contenidos](#-tabla-de-contenidos)
- [⚒ Requerimientos](#-requerimientos)
- [⚙ Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [⚽ Objetivos](#-objetivos)
- [🧮 Como funciona](#-como-funciona)
- [📟 Instalación](#-instalación)
- [📷 Capturas](#-capturas)


<!-- Requerimientos -->
## ⚒ Requerimientos

<ul>
  <li>Windows 8 o Superior</li>
  <li>macOS Catalina o Superior</li>
  <li>Linux: Ubuntu, Debian, CentOS, Fedora, etc.</li>
  <li>Python 3.10.8 o Superior</li>
  <li>Tkinter 8.6 o superior</li>
  <li>Graphviz 0.20 o superior</li>
  <li>Pillow 10.0.1 o Superior</li>
  <li>sv_ttk</li>
  <br>
  <li>Fuentes</li>
  <ul>
  <li>Montserrat </li>
  <li>Cascadia Code</li></ul>
  
</ul>

## ⚙ Tecnologías Utilizadas

<div align="center" style="display:flex;justify-content:center;gap:20px">
 <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,vscode,git,graphql" />
  </a>
</div>
<ul>
  <li>Python</li>
  <li>Visual Studio Code</li>
  <li>Git</li>
  <li>Graphviz</li>
</ul>

## ⚽ Objetivos
* **Objetivo General**
    * Diseñar y desarrollar una aplicación con entorno visual que contenga un analizador léxico que lea operaciones matematicas, junto con configuraciones para las gráficas.
* **Objetivos Específicos**
    * Elaborar un sistema que proporcione una interfaz agradable a la vista para interactuar con el analizador de una forma intuitiva.
    * Proporcionar herramientas para analizar un archivo `Json`.
    * Generar gráficas para la visualización correcta del orden de las opeaciones por medio de la libreria Graphviz de Python

## 🧮 Como funciona

<h3>Clase App</h3>

```python
class App(tk.Tk):
```
Esta clase se encarga de la interfaz gráfica, heredando elementos de tk, para poder utilizarlos dentro de la clase, aquí se definen
las propiedades básicas de la ventana, como el tamaño, el titulo de la ventana, el tema a utilizar, configuraciones de algunos elementos gráficos, etc.

<h3>Clase Contenido</h3>

```python
class Contendio(ttk.Frame):
```

Esta clase se encarga de crear un Frame principal, dentro del cual estarán todos los elementos visuales como: botoes, etiquetas, cuadros de text, etc.

<blockquote>

**Variables**

```python
self.tokens_totales = []
self.errores = []
self.archivo_actual = None
```
Las primeras dos variables se usan para poder obtener los datos del analizador lexico y ser
utilizados por las demás opciones que cuenta el programa. La tercera variable se usa para poder almacenar
la ruta del archivo actual con el cual se esta trabajando.

</blockquote>

<br>

<blockquote>

**Método crear_menu_superior**

```python
def crear_menu_superior(self):
```
Se encarga de crear un Frame para la parte superior donde se encuentran los botones de analizar, errores, y reporte. 
y de agregar el Frame al Frame principal

</blockquote>
<br>
<blockquote>

**Método crear_text**

```python
def crear_text(self):
```
Se encarga de crear un Frame, que se agrega debajo del frame del menu superior.
En este panel se agrega el contador de lineas de codigo, la etiqueta con el nombre del archivo actual,
el cuadro de texto donde se puede escribir el `Json` deseado, junto con
las barras para el desplazamiento dentro del cuadro de text

</blockquote>
<br>
<blockquote>

**Método cargar_datos**

```python
def cargar_datos(self):
```
Se encarga de poder obtener los datos al momento de cargar un arhivo para poder agregarlos al campo de texto.
Tambíen actualiza la ruta del archivo actual, para el momento de guardar.

</blockquote>
<br>
<blockquote>

**Método analizar_datos**

```python
def analizar_datos(self):
```

Se encarga de obtener lo que tiene el cuadro de texto aplicandole el método `.lower()` y enviarselo al analizador léxico y obtener los tokens y errores, que se encontraron en el codigo enviado,
para su uso en las demás opciones disponibles.

</blockquote>
<br>
<blockquote>

**Método crear_archiv_error**

```python
def crear_archivo_error(self):
```
Se encarga de crear un archivo con extensión `Json` con los errores encontrados durante el analisis del archivo

el archivo Json tiene el siguiente formato:
```json
{
    "errores": [
        {
            "No":1,
            "descripcion":{
                "lexema":"?",
                "tipo":"error lexico",
                "columna": 2,
                "fila": 9
            }
        }
    ]
}
```
</blockquote>
<br>
<blockquote>

**Método crear_reporte**

```python
def crear_reporte(self):
```
Se encarga de generar el grafico con las operaciones, tomando en cuenta las
configuraciones puestas en el codigo ingresado en el cuadro de texto.
Solamente se crea el grafico si ya se ha analizado el archivo una primera vez
de lo contarrio se lanza una alerta para indicar que no hay datos analizados
</blockquote>


<br>
<blockquote>

**Método guardar_como**

```python
def guardar_como(self):
```
Se encarga de guardar el contenido actual del cuadro de texto en un nuevo archivo con extesnión
`Json`, con la capacidad de que el usuario pueda elegir el nombre del archivo con el que lo desee
guardar
</blockquote>
<br>

<blockquote>

**Método guardar**

```python
def guardar_como(self):
```
Se encarga de guardar los cambios en el archivo cargado, a diferencia de la opción de guardar como,
no se genera un nuevo archivo, se usa el archivo cargado inicialmente o guardado con la opción anterior
para poder cargar el nuevo contenido dentro de ese archivo.
</blockquote>
<br>

<h3>Función para cargar el Json</h3>

```Python
def cargar_json(text_widget):
```

Esta función recibe como parametro el campo de texto dentro del cual necesitamos
ver el codigo que estamos abriendo.

La función abre una ventana donde se puede elegir cualquier archivo siempre y cuando su
extensión sea `.json`, para luego extraer la información del archivo y agregarla al cuadro de texto que
se paso por parametro

<h3>Clase Expression</h3>

```Python
class Expression(ABC):
```
Esta clase es la plantilla para las clases Token  para asegurar que se guarden
la fila y la columna del token encontrado

<h3>Clase Token</h3>

Se encarga de guardar los tokens reconocidos con el tipo y el valor propio del token.
Esta clase herada de la clase abstracta Expression, para guardar la fila y columna del token

<h3>Clase Error</h3>

Se encarga de guardar los errores encontrados con el No de error, el tipo , el valor propio del token.
y la fila y columa de los errores encontrados

<h3>Clase Analizador</h3>
Se encarga de analizar el contenido del cuadro de texto, teniendo diferentes
metodos para la realización del analisis.

<blockquote>

**Método leer_instrucciones**

```python
def leer_instrucciones(self):
```
Se encarga de gestionar los estados respectivos según el caracter leido, hace uso de un
bucle While que itera toda la cadena del cuadro de texto, usa un puntero y un estado, el puntero
es para poder manejar en que caracter se esta, y el estado va variando según el caracter leido
</blockquote>
<br>

<blockquote>

**Método limpiar**

```python
def limpiar(self):
```
Se encarga de limpiar los caracteres innecesarios como lo pueden ser las tabulaciones,
los saltos de línea o las tabulaciones, para quedar solo con el text que es relevante dentro
de nuestro archivo.
</blockquote>

<blockquote>

**Método crear_objeto**

```python
def crear_objeto(self):
```
Se encarga de añadir un token a la lista de tokens reconocidos, siempre y cuando el token
y la cadena sean diferentes de None
</blockquote>

<blockquote>

**Método crear_lexema**

```python
def crear_lexema(self):
```
Se encarga de crear lexemas cuando se envia un testo entre comillas, genera un error
si se agrega un caracter no alfanumerico por ejemplo: $,#,%,&,/, etc. Mediante un
bucle for se itera un listado de patrones, para poder obtener el tipo del lexema que se esta leyendo,
una vez completado el bucle se retorna el lexema encontrado.
</blockquote>
<br>

<blockquote>

**Método dos_valores**

```python
def dos_valores(self):
```
Se encarga de agregar los tokens de tipo número cuando se envia un numero, no importando si viene con o sin signo,
al tener solo un tipo de dato que se puede registrar.
</blockquote>
<br>

<blockquote>

**Método crear_numero**

```python
def crear_numero(self):
```
Se encarga de crear un numero, concatenado los caracteres que se tienen dentro del texto recibido,
se tiene en cuenta que no pueden venir más de un punto decimal, si viene más de un punto decimal se crea un error
pero no se concatena ese error, para poder omitir dicho punto adicional, una vez completado retorna un entero
o un decimal según sea el caso, si viene un punto decimal automaticamente es un flotante, si no posee un
punto para indicar los decimales se retorna un valor entero
</blockquote>
<br>

<blockquote>

**AFD**

![AFD](https://i.imgur.com/hY82WFp.png)
</blockquote>
<br>

<h3>Clase Instrucciones</h3>
Se encarga de operar las operaciones matematicas que se escriben en el cuadro de texto
que esta en la ventana principal del programa, cuenta con los siguientes métodos:

Recibe como parametro los tokens, que devuelve el analizador lexico.

Guarda información en las siguientes variables
```python
self.instrucciones = []
self.configuraciones = {
    TipoToken.PALABRA_CLAVE_TEXT: None,
    TipoToken.PALABRA_CLAVE_FONDO: None,
    TipoToken.PALABRA_CLAVE_FUENTE: None,
    TipoToken.PALABRA_CLAVE_FORMA: None,
    }
```
El diccionario usado es para poder guardar las diferentes configuraciones que posteriormente
se van a utilizar para generar el grafico, por ello, definimos una llaves predeterminadas
a su vez que las inicializamos con None, para no alterar los resultados

<blockquote>

**iniciar**
En este metodo se iteran los tokens para poder obtener unicamente aquellos tokens
que necesitamos para realizar las operaciones mátematicas, a su vez
que va guardando los resultados en una variable junto con la opreacion realizada, para poder ser
utilizada en la generación de la gráfica.

Luego de tener los datos necesarios se procede a generar la gráfica.
</blockquote>
<br>
<blockquote>

**operar**
En este método se crean los elementos necesarios para la gráfica, guardar las configuraciones
que estan en el cuadro de texto para las graficas, y finalmente retorna los valores númericos de las operaciones
El proceso seguido es primero encontrar si es una operacion o una configuracion.
Luego si es una operación númerica se procede a iterar los tokens para poder realizar una acción
dependiendo del token leido, si el token leido es solamente un número se agrega a una lista con los valores y a una lista que
contiene algunos tokens necesarios para la gráfica, si
el token es una llave de apertura "[" se procede a volver a llamar a operar, ya que 
se espera una nueva operación númerica.

Una vez completado los bucles para ver que operaciones se tienen que operar los valores, para esto
según el tipo de la operación se va viendo que valor retornar, luego de ver que opearación es y tener el valor
resultante de hacer dicha operación se procede a agregar a una variable temporal el valor de la operacion,
con su respectivo resultado
</blockquote>
<br>

<blockquote>

**llamar_grafica**
Este método se encarga de crear la gráfica llamando al método `generar_operaciones`
de la clase `Graph()`
</blockquote>
<br>

<h3>Clase Graph</h3>
El constructor de esta clase recibe datos, e instrucciones, donde los datos
son las configuraciones que se agregan en el cuadro de texto, y las instrucciones
son las operaciones que se van a mostrar.

Cuenta con 3 métodos los cuales trabajan en conjunto para genera la gráfica
<blockquote>

**generar_operaciones**

Se encarga de crear un subgráfico por cada operacion en la lista de operaciones.
</blockquote>
<br>

<blockquote>

**crear_nodos**

En esta parte se van creando los nodos de los gráficos, tiene en cuenta que hay operaciones que pueden tener
operaciones anidadas por lo que si encuentra una operacion con un valor que tenga una operación anidada, el método se vuelve
a llamar a si mismo para crear una recursividad y volver a crear los nodos de las operaciones anidadas.
El nombre de los nodos va dependiendo de 3 parametros: El no de operacion actual, la fila, y el número de nodo,
esto se realiza con el fin de no generar dos nodos con el mísmo nombre y susituir nodos que no se necesitan reemplar.
</blockquote>
<br>

<blockquote>

**cambiar_forma**

Este método existe para poder aceptar cualquier tipo de forma ya que al momento de pasar los parametros,
se le aplica un `.lower()` lo cual afecta a algunos nombre de figuras, por lo que si la forma enviada tiene alguna
letra mayuscula dentro de su declaració se compara su version con letras minusculas, y se le cambia por el valor original
que son nombres con algunas letras en mayusculas
</blockquote>
<br>

## 📟 Instalación
Descargue el código o bien clone el repositorio en una carpeta.

Si se opta por la clonación se hace con la siguiente linea de código en terminal (Antes de ejecutar el codigo asegurese de estar en la carpeta donde lo quiere descargar)

```bash
git clone https://github.com/J-Ajsivinac/LFP_S2_2023_Practica_202200135
```

## 📷 Capturas
![Captura 1](/img/menu.png)
<p align="center">Menú principal</p>

![Captura 2](/img/reportes.png)
<p align="center">Informe generado</p>
