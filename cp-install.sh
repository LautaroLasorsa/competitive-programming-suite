CP="$HOME/competitive-programming"
mkdir -p $CP

cp README.pdf "$CP/README.pdf"
mkdir -p $CP/bin
mkdir -p $CP/notebook

for ext in py cpp kt; do
    touch "$CP/notebook/template.$ext"
done

cp -p -r template-propuesta $CP/template-propuesta 

cd scripts/
for ext in sh py; do
    for x in *.$ext;do
        chmod +x $x
        cp $x "$CP/bin/${x%.*}"
    #    cp $x "$HOME/.local/bin/${x%.*}"
    done
done

cd ..

cp -r -p auxiliares/* "$CP/bin"

# Verifica si el directorio ya está en el PATH
if [[ ":$PATH:" != *":$CP:"* ]]; then
    # Si no está, agrega el directorio al PATH
    echo "export PATH=\"$CP:\$PATH\"" >> "$HOME/.bashrc"
    echo "export PATH=\"$CP/bin:\$PATH\"" >> "$HOME/.bashrc"
    echo "CP=\"$CP\"" >> "$HOME/.bashrc"

    export CP=$CP
    export PATH="$PATH:$CP:$CP/bin"
fi

# Crea aliases para poder utilizar los comandos con distintos nombres
echo "alias cp-py='cp-python'" >> "$HOME/.bashrc"
echo "alias cp-kt='cp-kotlin'" >> "$HOME/.bashrc"

cp -r -p template-propuesta "$CP/"

echo -e "\e[1;32mCompetitive programming suite se ha instalado exitosamente.\e[0m"
source "$HOME/.bashrc"
