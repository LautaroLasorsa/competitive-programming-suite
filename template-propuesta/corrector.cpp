#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <set>
#include <map>
#include <cstdlib>
#include <cassert>
#include <string>
#include <cstring>
#include <cmath>
#include <sstream>
#include <iomanip>

using namespace std;

#define esta(x,c) ((c).find(x) != (c).end())
#define forn(i,n) for(int i=0;i<int(n);i++)

#define ALL(c) begin(c), end(c)
#define SIZE(c) int((c).size())

typedef long long tint;

void finish(int score)
{
    cout << double(score) / 100.0 << endl;
    exit(0);
}

void fail()
{
    finish(0);
}


void check(bool assertion, int score = 0)
{
    if (!assertion)
        finish(score);
}

/*
    Un programa que evalua para cada caso comparandolo contra la salida de la solución
    oficial y le asigna un puntaje entre 0 (WA) y 100 (AC). Un puntaje intermedio se
    considerará PA.
*/

int main(int argc, const char *args[])
{
    /*
    args[1] = Datos de entrada
    args[2] = Datos de salida correctos (generados por la solución oficial)
    args[3] = Datos de salida de la solución a evaluar
    */

    assert(argc >= 4);
    // IN, DAT, OUT
    ifstream dat(args[1]), correctOutput(args[2]), contestantsOutput(args[3]);

    // La función finish termina la ejecución e imprime el puntaje asignado.
    finish(100);
    return 0;
}
