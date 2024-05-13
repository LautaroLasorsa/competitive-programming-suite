# competitive-programming-suite

 Un paquete de instalación de comandos útiles para programación competitiva

# Instalar el paquete

Para instalar el paquete ejecute en consola (WSL para usuarios Windows)

```sh
    git clone https://github.com/LautaroLasorsa/competitive-programming-suite.git
    cd competitive-programming-suit 
    sudo bash cp-install.sh
```

Esto además creara los siguientes archivos y directorios:
```sh
    /usr/local/competitive-programming/
    /usr/local/competitive-programming/notebook/
    /usr/local/competitive-programming/notebook/template.cpp
    /usr/local/competitive-programming/notebook/template.py
```

# Comandos

## cp-cpp

Este comando permite compilar y ejecutar contra los casos de prueba un archivo cpp 

```sh
    cp-cpp A
```

Compila el archivo A.cpp y lo ejecuta contra todos los archivos A*.in

Además, crea un archivo A.print que contiene el código ejecutado y todo lo mostrado por consola.

Se puede agregar un segundo parámetro opcional, para indicar si queremos solo compilar el archivo (generando el ejecutable A) o solo correr el ejecutable contra los casos de prueba.

```sh
    cp-cpp A build # Compilar
    cp-cpp A run   # Ejecutar
```

Solo la parte de Ejecutar crea el archivo A.print

## cp-python

Este comando permite ejecutar contra todos los casos de prueba un archivo .py (Python 3)

```sh
    cp-python A
```

Ejecuta el archivo A.py contra todos los archivos A*.in

Además, crea un archivo A.print que contiene el código ejecutado y todo lo mostrado por consola.

## cp-notebook

Este comando abre la carpeta ```/usr/local/competitive-programming/notebook``` en VS CODE.

## cp-template

Recibe un parametro opcional para indicar si utilizar el template de C++ o de Python.

```sh
    cp-template cpp A      # Copia template.cpp en A.cpp
    cp-template python A   # Copia template.py en A.py
```

Tener en cuenta que los templates instalados originalmente son archivos en blanco y hay que poner lo que queramos en ellos.

## cp-get-notebook

Permite acceder a notebooks de referencia que estén subidos a GitHub, abriendo el notebook en VS CODE. Si no existe, copia el repositorio como una carpeta dentro de ```/usr/local/competitive-programming```. 

```sh
    cp-get-notebook nombre 
```

Permite acceder al notebook indicado en el parámetro nombre.

Si se llama 

```sh
    cp-get-notebook
```

Lista los notebooks disponibles y una breve descripción de cada uno.
