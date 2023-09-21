<h1 align="center">Manual de Usuario</h1>

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
- [📖 Descripción](#-descripción)
- [⚒ Requerimientos](#-requerimientos)
- [🗂 Recursos](#-recursos)
- [📟 Instalación](#-instalación)
- [⚡ Inicio Rápido](#-inicio-rápido)
- [💻 Interfaz de Usuario y Funcionalidades](#-interfaz-de-usuario-y-funcionalidades)
  - [Parte superior](#parte-superior)
  - [Parte inferior](#parte-inferior)


<!-- Requerimientos -->
## 📖 Descripción
El programa es un analizador léxico con interfaz gráfica de archivos con extesnión JSON, donde los elementos dentro del archivo son operaciones mátematicas junto con configuraciones que se utilizan en la generación de una gráfica donde se ven las operaciones con ramificaciones según sea el caso.

El programa cuenta con 3 opciones principales, que son: analizar, errores y reporte. Tambíen cuenta con 3 opciónes para la gestión de archivos, las cuales son: Abrir, Guardar, Guradar Como. Finalmente se cuenta con la opción de Salir.

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

## 🗂 Recursos
<ul>
  <li><a href="https://www.python.org/downloads/">Python 3.10.8 o Superior</a></li>
  <li>pip install tkinter</li>
  <li><a href="https://pypi.org/project/graphviz/">Graphviz 0.20 o superior</a></li>
  <li><a href="https://pypi.org/project/Pillow/">Pillow 10.0.1 o Superior</a></li>
  <li>pip install sv-ttk</li>
  <br>
  <li>Fuentes</li>
  <ul>
  <li><a href="https://fonts.google.com/specimen/Montserrat">Montserrat </a></li>
  <li><a href="https://github.com/microsoft/cascadia-code">Cascadia Code</a></li>
  </ul>
  
</ul>

## 📟 Instalación
Descargue el código o bien clone el repositorio en una carpeta.

Si se opta por la clonación se hace con la siguiente linea de código en terminal (Antes de ejecutar el codigo asegurese de estar en la carpeta donde lo quiere descargar)

```bash
git clone https://github.com/J-Ajsivinac/LFP_S2_2023_Proyecto1_202200135.git
```

## ⚡ Inicio Rápido
Una vez con la carpeta del proyecto y teniendo los recursos, dirijase a donde está al archivo `main.py` y ejecutelo de la siguiente forma

```bash
python main.py
```

Luego se le abrirá la ventana principal

## 💻 Interfaz de Usuario y Funcionalidades
Al ejecutar la aplicación se desplegará la siguiente ventana, la cual es la principal:
![Captura 1](https://i.imgur.com/zbKGoTI.png)

La ventana principal esta dividida en dos partes principales:

### Parte superior
En la parte superior se tiene 4 botones.

> El primer botón el cual tiene como icono una casa da acceso a un
> submenu donde podemos encontrar las opciones de:
> ![Captura 2](https://i.imgur.com/aUw0D28.png)
> * Abrir: Despliega una ventana donde se puede elegir un archivo que tenga el formato JSON
> ![Captura 3](https://i.imgur.com/8j2IFtK.png)
> * Guardar: Al presionar esta opción se guardaran los cambios hechos en el area de texto en el documento actual (El documento debe haberse guardado como, o abierto con la opción anterior). Al darle clic a esta opción y finalizar el guardado se le enviara un mensaje de que el documento se ha guardado
> ![Captura 3](https://i.imgur.com/sqPrITN.png)
> 
> * Guardar Como: Guarda el contenido del area de texto, a un archivo nuevo, para ello se abre una ventana similar a la que se abrio en la parte de abrir, pero se le pide al usuario colocar un nombre para guardar el contenido a un documento con ese nombre
>![Captura 3](https://i.imgur.com/qZVpwCC.png)
> 
> * Salir: Al seleccionar esta opción la aplicación se cierra

Con el botón analizar se despliega una nueva ventana donde se pueden visualizar los elementos reconocidos dentro del texto existente en el cuadro de texto junto con información como la fila, columna y el tipo.
![Captura 4](https://i.imgur.com/hPtFdYR.png)

Con el botón Errores se crea un archivo con los errores encontrados durante el analisis, el archivo resultante está en formato JSON, y se abrira luego de presionar el botón (La aplicación con la cual se abra el archivo depende cual este definida en el sistema en el cual se esta utilizando)

El formato del archivo de salida es el siguiente:

```json
{
    "errores": [
        {
            "No": 1,
            "descripcion": {
                "lexema": "#",
                "tipo": "Error Léxico",
                "columna": 15,
                "fila": 2
            }
        },
        {
            "No": 2,
            "descripcion": {
                "lexema": "#",
                "tipo": "Error Léxico",
                "columna": 29,
                "fila": 4
            }
        }
    ]
}
```

Con el botón Reporte se genera un grafico con las operaciones que están dentro del cuadro de texto, el gráfico que se genera es similar al siguiente (Varia según las operaciones que se les agregue):

![Captura 5](https://i.imgur.com/RbjhXve.png)

Es importante definir las configuraciones iniciales dentro del cuadro de texto, para poder visualizar de forma personalizada la gráfica (se dará más información del contenido que debe estar ingresado en el cuadro de texto en el siguiente apartado)
### Parte inferior
La parte Inferior Está conformada por 2 filas importantes, la primera donde se puede visualiza el nombre del archivo actual junto con su extención (Al inicio el nombre es Nuevo Documento.json)
![Captura 6](https://i.imgur.com/a4vwpUm.png)

La 2 fila es en donde se ve un contador de lineas de código un cuado de texto donde se puede escribir el código a analizar, y dos barras de desplazamiento para poder mover el código según sean las necesidades

![Captura 7](https://i.imgur.com/k3CkE7j.png)

El formato para que trabaje optimamente el analizador es:
```json
{
    "operaciones": [
        {
            "operacion": "Suma",
            "valor1": 2.2,
            "valor2": 2
        },
        {
            "operacion": "resta",
            "valor1": 4.5,
            "valor2": [
                {
                    "operacion": "potencia",
                    "valor1": 10,
                    "valor2": 3
                }
            ]
        },
        {
            "operacion": "resta",
            "valor1": 7,
            "valor2": 3
        }
    ],
    "configuraciones": [
        {
            "texto": "Operaciones",
            "fondo": "gray",
            "fuente": "white",
            "forma": "rect"
        }
    ]
}
```

Lo que está escrito en texto, se usará como nombre del archivo junto con el encabezado principal de las gráficas

Para la parte de las configuraciones del formato anterior es importante tener en cuenta que la librería usada para la graficación solo toma colores escritos en inglés por lo cual es importante ingresar bien los nombres, al igual que las formas. [ver formas](https://graphviz.org/doc/info/shapes.html)

