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

import sys
from PySide6.QtWidgets import QApplication
from rascally_ui.rascallyUI import Rascally_UI

#########################################################
#       MAIN
#########################################################
if __name__ == '__main__':
    app = QApplication(sys.argv)

    rascal = Rascally_UI()
    rascal.show()

    sys.exit(app.exec())