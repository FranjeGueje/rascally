#!/bin/bash

# shellcheck source=/dev/null
source .venv/Scripts/activate

pyinstaller --onefile rascal_gui.py

exit 0
