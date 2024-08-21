
cd "$CP"
algun_notebook=false

if [ "$1" = "vasito" ] || [ "$1" = "all" ]; then
    if [ ! -d "icpc-team-notebook-el-vasito" ]; then
        git clone https://github.com/mhunicken/icpc-team-notebook-el-vasito.git
    fi 
    
    if [ "$1" != "all" ];then
        cd icpc-team-notebook-el-vasito/
        code .
    fi
    algun_notebook=true
fi

if [ "$1" = "python-unlam" ] || [ "$1" = "all" ]; then
    if [ ! -d "notebook-unlam-python" ]; then
        git clone https://github.com/LautaroLasorsa/notebook-unlam-python.git
    fi
    if [ "$1" != "all" ];then
        cd notebook-unlam-python/
        code .
    algun_notebook=true
    fi
fi

if [ "$1" = "all" ]; then
    echo "Todos los notebooks han sido descargados."
    code .
fi

if [ "$algun_notebook" = false ]; then
    echo "Listas de notebooks disponibles:
        all: Descarga todos los notebooks disponibles.
        vasito : Notebook del equipo de ICPC GGDem de la Universidad Nacional de Córdoba (UNC)
        python-unlam : Notebook realizado para los equipos formados en el curso ICPC UNLaM (Universidad Nacional de La Matanza) que decidieron utilizar Python.
    "
fi
