#!/bin/bash

# shellcheck source=/dev/null
source .venv/bin/activate
pyinstaller --onefile rascally_gui.py

exit 0
