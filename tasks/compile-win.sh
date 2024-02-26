#!/bin/bash

# shellcheck source=/dev/null
source .venv/Scripts/activate

function compila {
    directorio=$(dirname "$(readlink -f "$1")")
    nombre=$(basename "$1")
    nombre_base="${nombre%.*}"
    extension="${nombre##*.}" # Obtener la extensión del archivo

    case "$extension" in
    "ui")
        echo "!Compilando: $1"
        pyside6-uic "$1" -o "$directorio""/""$nombre_base"".py"
        ;;
    "qrc")
        echo "!Compilando: $1"
        pyside6-rcc "$1" -o "./""$nombre_base""_rc.py"
        ;;
    *)
        echo -e "\tOmitiendo: $1"
        ;;
    esac
}

for archivo in "$1"/*; do
    compila "$archivo"
done

exit 0
