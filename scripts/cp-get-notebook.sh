
cd "$CP"
if [ "$1" = "vasito" ]; then
    if [ ! -d "icpc-team-notebook-el-vasito" ]; then
        git clone https://github.com/mhunicken/icpc-team-notebook-el-vasito.git
    fi 
    cd icpc-team-notebook-el-vasito/
    code .
else
    echo "Listas de notebooks disponibles:
        vasito : Notebook del equipo de ICPC GGDem de la Universidad Nacional de Córdoba (UNC)
    "
fi
