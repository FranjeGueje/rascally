# 
# Copyright (C) 2024 Paco Guerrero <fjgj1@hotmail.com>
# 
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
#############################################################################################
# Rascally
# https://github.com/FranjeGueje/rascally
#############################################################################################

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QDialog, QDialogButtonBox
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
import resources_rc
import sys

class RascalDialog(QDialog):
    def __init__(self, mensaje: str, tipo='I', parent=None) -> None:
        super().__init__(parent=parent)
        self.resize(240, 120)
        self.setWindowTitle("Rascally Dialog")
        self.setStyleSheet('background-color: rgb(36, 12, 36);color: white;')

        # Creamos un layout vertical
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Añadimos una etiqueta con el mensaje
        layout.addWidget(QLabel(mensaje))
        
        run = True
        if isinstance(tipo, str):
            if tipo == 'E':
                botones = QDialogButtonBox(QDialogButtonBox.Ok)
                botones.accepted.connect(self.accept)
            elif tipo == 'Q':
                # Creamos los botones predeterminados (Aceptar y Cancelar)
                botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                # Conectamos los botones a sus respectivas funciones
                botones.accepted.connect(self.accept)
                botones.rejected.connect(self.reject)
                run = False
            else:
                botones = QDialogButtonBox(QDialogButtonBox.Ok)
                botones.accepted.connect(self.accept)
        else:
            botones = QDialogButtonBox(QDialogButtonBox.Ok)
            botones.accepted.connect(self.accept)

        # Añadimos los botones al layout
        layout.addWidget(botones)
        
        if run:
            self.exec()
