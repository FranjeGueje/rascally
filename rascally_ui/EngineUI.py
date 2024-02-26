
from typing import List

from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

from ui.Engine import Ui_EngineUI
from rascally.engines import LauncherEngine

class EngineFrame(QFrame, Ui_EngineUI):
    signal_engine = Signal(LauncherEngine)
    def __init__(self, engine: LauncherEngine):
        super().__init__()
        self.setupUi(self)
        self.engine = engine
        
        self.pushButton.setText(self.engine.name)
        if self.engine.name == 'Epic':
            icon = ':/engines/assets/epic.png'
        elif self.engine.name == 'Ubisoft':
            icon = ':/engines/assets/ubisoft.png'
        elif self.engine.name == 'Link':
            icon = ':/engines/assets/link.png'
        self.pushButton.setIcon(QIcon(icon))
        
        self.pushButton.clicked.connect(self.activate_engine)
        
    def activate_engine(self) -> LauncherEngine:
        self.signal_engine.emit(self.engine)