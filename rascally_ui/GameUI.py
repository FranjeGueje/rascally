import os
import glob

from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

from ui.GameFrame import Ui_GameFrame
from rascally_ui.RascalDialog import RascalDialog
from rascally.engines import BasicGame
from rascally.steam_core.steam_utils import exe_in_games
from rascally import Rascally


class GameFrame(QFrame, Ui_GameFrame):
    signal_adding = Signal(BasicGame)
    def __init__(self,game: BasicGame, rascal: Rascally):
        super().__init__()
        self.setupUi(self)
        self.game = game
        self.rascal = rascal
        
        self.title_label.setText(self.game.AppName)
        self.compatdata_label.setText(f'From COMPAT_DATA:\n{self.get_compatDataPath()}')
        self.rascal.download_thumbnails(self.game)
        self.set_img()
        
        self.img_button.clicked.connect(self.selected)
        self.exclude_button.clicked.connect(self.excluded)
        self.show()
    
    def get_compatDataPath(self):
        return f'{os.path.basename(self.game.CompatData)}'
    
    def set_img(self) -> None:
        name_file = self.game.AppName
        image = f'{self.rascal.cache_dir}/{name_file}.*'
        file_image = glob.glob(image)
        if file_image:
            self.img_button.setIcon(QIcon(file_image[0]))
    
    def selected(self) -> None:
        games = self.rascal.get_nonsteam_games()
        if exe_in_games(games,self.game.Exe):
            dialogo = RascalDialog(mensaje="""WARNING!
This games has been found in a Steam library. The game could be DUPLICATED.

ARE YOU SURE you want to add this game?""", tipo='Q')
            if dialogo.exec():
                self.signal_adding.emit(self.game)
        else:
            dialogo = RascalDialog(
                mensaje='Are you sure you want to add this game to your Steam library?',
                tipo='Q')
            if dialogo.exec():
                self.signal_adding.emit(self.game)
    
    def excluded(self) -> None:
        dialogo = RascalDialog(
            mensaje="""If you add an exception to this COMPATDATA it will not show any game that is in it.
Are you sure you want to add this compatdata as an exception?""",
            tipo='Q')
        if dialogo.exec():
            self.rascal.add_exception(self.get_compatDataPath())