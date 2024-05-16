CP="$HOME/competitive-programming"

mkdir -p $CP/bin
mkdir -p $CP/notebook
touch $CP/notebook/template.py 
touch $CP/notebook/template.cpp
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

    export $CP
    export PATH="$PATH:$CP:$CP/bin"
fi

cp -r -p template-propuesta "$CP/"