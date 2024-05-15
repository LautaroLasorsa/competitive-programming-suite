#!/usr/bin/python3 -B
'''MIT License

Copyright (c) 2017 Martin Villagra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Modified by Carlos Miguel Soto in 2023
Modified by Agustin Santiago Gutierrez in 2018-2024
'''
from __future__ import print_function
from collections import defaultdict
from contextlib import contextmanager
import subprocess, sys
import os, time
from sys import argv
import importlib.util
import run
import re
assert sys.version_info.major >= 3

VERSION = "1.5"
DEFAULT_TIME_LIMIT = 4
CASDIR = "casos"
GENDIR = os.path.join("casos", "generados")
VERDIR = os.path.join("casos", "verificadores")
CONFIGFILE = "config.json"
GRADERS = ["graders/grader.cpp"]
SOLDIR = "soluciones"
CORNOMBRE = "corrector"
CASOSZIP = 'casos.zip'
REFSOL = 'referencia'
IN_EXT = '.in'
DAT_EXT = '.dat'
DEFAULT_EXE_EXT = '.exe'
EXE_EXTS = [DEFAULT_EXE_EXT,'.class']
EJECUTABLES = [".cpp", ".cxx", ".py", ".pas", ".java"]
VERBOSE = False

def main(argv):
    comandos = { #nombre : (descripcion, funcion)
        "limpiar" : ("quitar ejecutables y casos creados por generadores", limpiar),
        "generar" : ("ejecutar generadores", generar),
        "verificar" : ("ejecutar verificadores de casos", verificar),
        "resolver" : ("ejecutar las soluciones", resolver),
        "empaquetar" : ("crea un zip con los casos", empaquetar),
        "zippear" : ("crea un zip listo para subir", zippear),
        "todo" : ("limpiar, generar, verificar y resolver", todo),
    }
    abreviaciones = {
        "l" : "limpiar",
        "g" : "generar",
        "v" : "verificar",
        "r" : "resolver",
        "e" : "empaquetar",
        "z" : "zippear",
        "t" : "todo",
    }
    VERBOSE_ARG = "--verbose"
    def usage():
        print("uso: hace.py [" + VERBOSE_ARG + "] <operacion>")
        print("operaciones disponibles:")
        print('\n'.join(
            [ "\t" + RESET + BOLD + RED + op + ", " + abreviaciones[op] #prints shortcut and name
            + "\n\t\t" + RESET + comandos[abreviaciones[op]][0] #prints description
                for op in ["l", "g", "v", "e", "r", "t"]]
        ))
        print("version "+VERSION)
        exit(1)
    if VERBOSE_ARG in argv:
        global VERBOSE
        VERBOSE = True
        argv = [arg for arg in argv if arg!=VERBOSE_ARG]
    if len(argv) != 2:
        usage()

    comando = argv[1]
    if comando in abreviaciones:
        comando = abreviaciones[comando]

    if comando not in comandos:
        print("comando invalido")
        usage()

    if not os.path.isdir(CASDIR):
        print("carpeta casos inexistente")
        exit(1)
    comandos[comando][1]()
    print(RESET, end='')


def get_problem_name():
    return os.path.basename(os.getcwd())


def listar_archivos_en(nombredir, criterio):
    archivos = []
    if os.path.isdir(nombredir):
        for x in os.listdir(nombredir):
            x = os.path.join(nombredir, x)
            if os.path.isfile(x) and criterio(x):
                archivos.append(x)
    return archivos

def limpiar():
    def borrar_archivos_en(nombredir, criterio):
        for x in listar_archivos_en(nombredir, criterio):
            os.remove(x)
    temp_tex = lambda x: obtener_ext(x) in [".bak", ".aux", ".log", ".sav", ".fdb_latexmk", ".fls"] 
    borrar_archivos_en("img", temp_tex)
    borrar_archivos_en(".", temp_tex)

    archivos_dat = lambda x: obtener_ext(x)==DAT_EXT
    borrar_archivos_en(CASDIR, archivos_dat)

    archivos_casos = lambda x: obtener_ext(x) in EXE_EXTS + [IN_EXT, DAT_EXT]
    borrar_archivos_en(GENDIR, archivos_casos)
    borrar_archivos_en(SOLDIR, archivos_casos)
    borrar_archivos_en(VERDIR, archivos_casos)

    def remove_if_exists(file):
        if os.path.isfile(file):
            os.remove(file)

    for ext in EXE_EXTS:
        remove_if_exists(CORNOMBRE+ext)
    remove_if_exists(CASOSZIP)

    problem_name = get_problem_name()
    remove_if_exists(problem_name + ".zip")

def compilar(fuente, verboso=False, estatico=False):
    nombre, ext = os.path.splitext(fuente)
    exe = nombre + DEFAULT_EXE_EXT
    if ext==".cpp" or ext==".cxx":
        comando = ["g++", "-O2", "-std=gnu++14", fuente, "-o", exe]
    elif ext==".py":
        return fuente
    elif ext==".pas":
        comando = ["fpc", fuente, "-o"+exe]
    elif ext==".java":
        comando = ["javac", fuente]
        exe = nombre + ".class"
    else:
        raise RuntimeError("Extension "+ext+" desconocida")
    if estatico:
        comando+=["-static"]
    if VERBOSE:
        print(decir_cmd(comando))
    try:
        with open(os.devnull, "w") as ignorar:
            subprocess.check_call(comando, stderr = None if VERBOSE else ignorar, stdout = None if VERBOSE else ignorar)
        return exe
    except subprocess.CalledProcessError:
        raise ErrorCompilacion

def hacer_comando_ejecucion(archivo):
    ext = obtener_ext(archivo)
    comando = []
    if ext=='.py':
        comando.append(sys.executable or 'python3')
    if ext=='.class':
        comando.append("java")
        comando.append("-cp")
        comando.append(SOLDIR)
        archivo = archivo[len(SOLDIR)+1:-6]
    comando.append(archivo)
    return comando

def ejecutar(archivo, entrada=None, salida=None, params=[], mostrarErrores=False):
    comando = hacer_comando_ejecucion(archivo)+params
    if entrada is not None: entrada = open(entrada, "r")
    if salida is not None: salida = open(salida, "w")
    try:
        with open(os.devnull, "w") as ignorar:
            subprocess.check_call(comando, stderr = None if mostrarErrores or VERBOSE else ignorar
                                    , stdin = entrada
                                    , stdout = salida)
    finally:
        if entrada is not None: entrada.close()
        if salida is not None: salida.close()

def generar_entradas_en(fdir):
    # Genera los .in
    for x in listar_archivos_en(fdir, lambda x: obtener_ext(x) in EJECUTABLES):
        print(RESET + BOLD + "Generando .in's con " + RESET + decir_nombre(os.path.basename(x)))
        with cd(fdir):
            try:
                ejecutar(compilar(os.path.abspath(os.path.relpath(x, fdir))))
            except ErrorCompilacion:
                print(RESET + BOLD + RED + "Fallo compilacion")
            except subprocess.CalledProcessError:
                print(RESET + BOLD + RED + "Error de ejecucion")

def generar_salidas_en(fdir):
    # Genera los .dat, ejecutando la solucion llamada referencia o la primera lexicograficamente menor si esta no existe
    sols = sorted(listar_archivos_en(SOLDIR, lambda x: obtener_ext(x) in EJECUTABLES))
    if sols:
        ref_src = next((s for s in sols if os.path.splitext(os.path.basename(s))[0]==REFSOL), sols[0])
        print(RESET + BOLD + "Generando .dat's de", fdir, "con " + RESET + decir_nombre(os.path.basename(ref_src)))
        try:
            ref_exe = os.path.abspath(compilar(ref_src))
        except ErrorCompilacion:
            print(RESET + BOLD + RED + "Fallo compilacion")
        for entrada in sorted(listar_archivos_en(fdir, lambda x: obtener_ext(x)==IN_EXT)):
            salida = os.path.splitext(entrada)[0]+DAT_EXT
            try:
                    ejecutar(ref_exe, entrada, salida)
            except subprocess.CalledProcessError:
                print(RESET + BOLD + RED + "Error de ejecucion en", entrada)

    else:
        print(RESET + BOLD + RED + "No hay solucion.")

def generar():
    # Genera .in y .dat
    if os.path.isdir(GENDIR):
        generar_entradas_en(GENDIR)
        generar_salidas_en(GENDIR)
    if os.path.isdir(CASDIR):
        generar_salidas_en(CASDIR)

    # Busca y compila el corrector
    for ext in EJECUTABLES:
        if os.path.isfile(CORNOMBRE+ext):
            print(RESET + BOLD + "Compilando corrector " + decir_nombre(CORNOMBRE+ext))
            compilar(CORNOMBRE+ext, True)
            break

def verificar_archivo_basico(archivo):
    doubleSpaces = False
    emptyLines = False
    startSpace = False
    endSpace = False
    endLine = False
    count = 0
    with open(archivo, 'r+') as fin:
        for l in fin:
            count = count + 1
            if(len(l) > 0 and l[-1] != '\n'): endLine = True
            if(len(l) and l[-1] == '\n'): l=l[:-1]
            if (len(l) > 0 and l[0] == ' '): startSpace = True
            if (len(l) > 1 and l[-1] == ' '): endSpace = True
            if "  " in l: doubleSpaces = True
            if (len(l) < 1): emptyLines = True
    quejas = []
    if (count == 0): quejas.append("0 lineas")
    if (startSpace): quejas.append("lineas con espacios al principio")
    if (endSpace): quejas.append("lineas con espacios al final")
    if (doubleSpaces): quejas.append("lineas con doble espacios")
    if (emptyLines): quejas.append("lines vacias")
    if (endLine): quejas.append("falta fin de linea al final")
    return quejas

def verificar_en(fdir):
    l = sorted(listar_archivos_en(fdir, lambda x: obtener_ext(x) in [IN_EXT, DAT_EXT]))
    print(RESET + BOLD + str(int(len(l)/2)), "casos encontrados" + RESET + " en carpeta " + fdir + RESET + (", verificando..." if len(l) else ""))
    for x in l:
        quejas = verificar_archivo_basico(x)
        if quejas:
            print(RESET + BOLD, x, "tiene:"+RED, ', '.join(quejas), RESET)


class ResultadosEjecucion:
    def __init__(self):
        self.errs = []
        self.partials = []
        self.cuenta = defaultdict(int)
    
    def log_cuenta(self, result, nombre):
            if result not in ["AC", "OK"]:
                if result == "PA":
                    color = YELLOW
                    self.partials.append((result, nombre))
                else:
                    color = RED
                    self.errs.append((result, nombre))
            else:
                color = GREEN
            print(RESET + BOLD + color + result[0], end='')
            self.cuenta[result] += 1

    def imprimir_resumen(self, casos=["AC", "PA", "TL", "RE", "WA"], end="\n"):
            def cond_color(color, num, post):
                return RESET + (BOLD + color if num>0 else "") + str(num) + post
            slash = RESET + BOLD + " / "
            resumen = slash.join([cond_color(GREEN if st in ["AC", "OK"] else RED, self.cuenta[st],st[0]) for st in casos])
            print("\t"+resumen+RESET, end=end)
    
    def imprimir_problemas(self):
        done = 0
        for e,y in self.errs + self.partials: # Solia mostrar solo los primeros 5
            if done > 0:
                print(" ", end="")
            col = YELLOW if e == "PA" else RED
            print(RESET + col + BOLD + e + RESET + BOLD + " en " + RESET + y, end="")
            done += 1
            if done % 8 == 0:
                print()
                done = 0
        if done > 0:
            print()
        #if len(self.errs) > 5:
        #    print(RESET + BOLD + "Problemas en " + RESET + str(len(self.errs)-5) + BOLD + " mas...")

def obtener_todos_los_casos():
    return sorted(obtener_casos(CASDIR)+obtener_casos(GENDIR), key=lambda x:x[0])

def ejecutar_chequeadores(fdir):
    casos = obtener_todos_los_casos()
    for fuente in listar_archivos_en(fdir, lambda x: obtener_ext(x) in EJECUTABLES):
        print(RESET + BOLD + "Ejecutando verificador " + RESET + decir_nombre(os.path.basename(fuente)))
        try:
            ejecutable = os.path.abspath(compilar(fuente))
        except ErrorCompilacion:
            print(RESET + BOLD + RED + "Fallo compilacion")
        stats = ResultadosEjecucion()
        for nombre, entrada, _ in casos:
            try:
                print(RESET + RED, end='')
                sys.stdout.flush()
                ejecutar(ejecutable, entrada, mostrarErrores=True)
                stats.log_cuenta("AC", nombre)
            except subprocess.CalledProcessError:
                stats.log_cuenta("RE", nombre)
        stats.imprimir_resumen(casos=["AC","RE"])
        stats.imprimir_problemas()

def verificar():
    verificar_en(CASDIR)
    verificar_en(GENDIR)
    if os.path.isdir(VERDIR):
        ejecutar_chequeadores(VERDIR)

def obtener_casos(fdir):
    casos = []
    for entrada in sorted(listar_archivos_en(fdir, lambda x: obtener_ext(x)==IN_EXT)):
        basepath = os.path.splitext(entrada)[0]
        salida = basepath+DAT_EXT
        if os.path.isfile(salida):
            casos.append((os.path.basename(entrada), entrada, salida))
    return casos

def resolver():
    if not os.path.isdir(SOLDIR):
        print("no hay soluciones")
        return
    casos = obtener_todos_los_casos()
    checker_path = CORNOMBRE+DEFAULT_EXE_EXT
    checker = os.path.abspath(checker_path) if os.path.isfile(checker_path) else None
    for x in sorted(listar_archivos_en(SOLDIR, lambda x: obtener_ext(x) in EJECUTABLES and os.path.basename(os.path.splitext(x)[0])!=REFSOL)):
        time_limit = DEFAULT_TIME_LIMIT
        print(RESET + BOLD + "Solucion " + decir_nombre(os.path.basename(x)))
        try:
            ref_exe = compilar(x)
            comando = hacer_comando_ejecucion(ref_exe)
            maxtime = 0
            pts = 0.0
            stats = ResultadosEjecucion()
            for nombre, entrada, salida in casos:
                res = run.run_solution(comando[0], comando[1:], entrada, None, salida, time_limit, checker=checker)
                if res.status != "TLE": maxtime = max(maxtime, res.running_time)
                pts += res.pts
                stats.log_cuenta(res.status, nombre)
            if casos: pts = pts*100.0/len(casos)
            stats.imprimir_resumen(end='')
            extraString = ""
            for message, source in [("failed", stats.errs), ("partial in", stats.partials)]:
                problematic_subtasks_strings = set(psub for e,y in source for psub in re.findall("S[0-9a-z]+", y))
                problematic_subtasks = set(c for s in problematic_subtasks_strings for c in s if c != 'S')
                extraString += (" {} subtasks: {}".format(message, " ".join(sorted(problematic_subtasks))) if problematic_subtasks else "")
            print("\t(" + BLUE + BOLD, round(pts), RESET + "pts,", "{0:0.2f}s".format(maxtime), ")" + extraString)
            stats.imprimir_problemas()
        except ErrorCompilacion:
            print(RESET + BOLD + RED + "Fallo compilacion")
    
def empaquetar():
    def casos_en(carpeta):
        return [os.path.join(carpeta, "*")+IN_EXT, os.path.join(carpeta, "*"+DAT_EXT)]
    comando = "zip"
    params=["-jTq", CASOSZIP]
    for _, entrada, salida in obtener_todos_los_casos():
        params.append(entrada)
        params.append(salida)
    if VERBOSE:
        print(decir_cmd([comando]+params))
    try:
        ejecutar(comando, params=params, mostrarErrores=True)
    except subprocess.CalledProcessError:
        print(RESET + BOLD + RED + "Fallo compresion")


def empaquetar_kit():
    comando = "zip"
    problem_name = get_problem_name()
    params = ["-jTq", f"kits/{problem_name}-cpp.zip"]
    for fil in os.listdir("kits"):
        params.append(f"kits/{fil}")
    if VERBOSE:
        print(decir_cmd([comando]+params))
    try:
        ejecutar(comando, params=params, mostrarErrores=True)
    except subprocess.CalledProcessError:
        print(RESET + BOLD + RED + "Fallo empaquetar kit")

def zippear():
    empaquetar_kit()
    comando = "zip"
    problem_name = get_problem_name()
    params = ["-qr", problem_name + ".zip", CASOSZIP, f"kits/{problem_name}-cpp.zip", *GRADERS, CONFIGFILE, f"{problem_name}.pdf", CORNOMBRE + ".cpp"]
    if VERBOSE:
        print(decir_cmd([comando]+params))
    try:
        ejecutar(comando, params=params, mostrarErrores=True)
    except subprocess.CalledProcessError:
        print(RESET + BOLD + RED + "Fallo empaquetar")

def todo():
    print(RESET+"limpiando...")
    limpiar()
    print(RESET+"generando...")
    generar()
    print(RESET+"verificando...")
    verificar()
    print(RESET+"resolviendo...")
    resolver()
    print(RESET+"empaquetando...")
    empaquetar()
    print(RESET+"zippeando...")
    zippear()

def obtener_ext(archivo):
    return os.path.splitext(archivo)[1]

@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)

class ErrorCompilacion(Exception):
    pass
        
RESET = '\x1b[0m'
BOLD = '\x1b[1m'
UNDERLINE = '\x1b[4m'
RED = '\x1b[31m'
GREEN = '\x1b[32m'
YELLOW = '\x1b[33m'
BLUE = '\x1b[34m'

def decir_nombre(name):
    return YELLOW + BOLD + "[" + name + "]"

def decir_cmd(cmd):
    return BLUE + BOLD + "$ " + RESET + ' '.join(cmd)

if __name__ == "__main__":
    main(argv)
