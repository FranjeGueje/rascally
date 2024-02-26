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