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
