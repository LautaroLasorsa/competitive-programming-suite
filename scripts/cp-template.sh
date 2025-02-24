if [ "$1" = "python" ] || [ "$1" = "py" ]; then
    cp "$CP/notebook/template.py"  "$2".py
elif [ "$1" = "cpp" ]; then
    cp "$CP/notebook/template.cpp" "$2".cpp
elif [ "$1" = "kt" ] || [ "$1" = "kotlin" ]; then
    cp "$CP/notebook/template.kt" "$2".kt
else
    echo -e "\e[31mInvalid language | Lenguaje inválido\e[0m"
    echo """Valid languages | Lenguajes validos: 
    -   python | py => "$CP/notebook/template.py"
    -   cpp         => "$CP/notebook/template.cpp"
    -   kotlin | kt => "$CP/notebook/template.kt"
    """
fi
