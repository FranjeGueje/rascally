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