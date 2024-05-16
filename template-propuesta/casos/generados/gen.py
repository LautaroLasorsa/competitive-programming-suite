import random
import string
from dataclasses import dataclass
from random import randint
from tqdm import tqdm # pip install tqdm

random.seed(832493274)

SUBTAREAS = 7

def toalpha(i: int) -> str:
    if i < 10:
        return str(i)
    return string.ascii_lowercase[i-10]

class Caso:
    def __init__(self):
        
        # Recibe (posiblemente) parametros y crea un caso de prueba con esos parametros

        self.checkvalid()

    def checkvalid(self):
        
        # Debe verificar si el caso es un caso valido

    def subtask(self, i: int):
        
        # Debe indicar si el caso pertenece a la subtarea i
         
        assert False

    def filename(self, cas: int):
        filename = "S"
        for i in range(1, SUBTAREAS+1):
            if self.subtask(i):
                filename += toalpha(i)
        filename += f"E{cas+1}.in"

        # Crea el nombre del archivo de la forma
        # S{Índices de subtareas que cumple}E{Número de caso}.in

        return filename

    def tostr(self) -> str:
        s = ""

        # Devuelve el caso formateado como string, debe ser la forma en
        # la que queremos que se imprima en el archivo .in

        return s

CASOS: list[Caso] = [
    #Una lista que contiene todos los casos generados para el problema
]

def write_casos():
    i = 0
    per_case = dict()
    for subtask in range(1, SUBTAREAS+1):
        per_case[subtask] = 0
    for caso in tqdm(CASOS):
        for subtask in range(1, SUBTAREAS+1):
            if caso.subtask(subtask):
                per_case[subtask] += 1
        filename = caso.filename(i)
        with open(filename, 'w') as f:
            f.write(caso.tostr())
        i += 1
    for k in per_case:
        print(f"subtask {k} = {per_case[k]}")

def main():
    write_casos()

if __name__ == "__main__":
    main()
