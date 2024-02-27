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

import os
import threading
import time

from PySide6.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QVBoxLayout, QListWidgetItem, QFileDialog
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QMouseEvent, QCursor

from ui.Rascally import Ui_Rascally
import util
from rascally.engines import CLONE_BALANCED, CLONE_FULL, CLONE_SYMLINK
from rascally_ui.EngineUI import EngineFrame
from rascally_ui.GameUI import GameFrame
from rascally_ui.RascalDialog import RascalDialog
from rascally import Rascally, LauncherEngine, BasicGame

name = 'Rascally'
version = '0.1.1'

class Rascally_UI(QMainWindow, Ui_Rascally, Rascally):

    def __init__(self, config_path=os.environ.get("HOME") + "/.config/rascally.conf"):
        super().__init__()
        self.setupUi(self)
        Rascally.__init__(self, config_path)

        # Main program
        self.setWindowTitle(f"{name} - {version}")
        self.title.setText(f"{name} - {version}")
        self.stackedWidget.setCurrentWidget(self.Wwelcome)

        # Ponemos la ventana sin barra de ventana, transludido el fondo
        # y con sombras
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 150))
        self.setGraphicsEffect(self.shadow)
        # Preparar el movimiento scroll del Área de juego
        self.last_pos = None
        self.gameArea.mouseMoveEvent = self.scrollMoveEvent
        self.gameArea.mousePressEvent = self.scrollEvent
        
        # Load the engines
        self.load_enginesUI()
        self.__prepare_gameList()
        self.__active_engine = None
        
        # Cargamos la config
        self.load_config_ui()
        
        # Es un grid válido?
        self.grid_valid = self.__is_grid_valid()

        # * CONEXIONES DE EVENTOS
        self.config_button.clicked.connect(self.config_show)
        self.close_btn.clicked.connect(self.__dialog_close)
        # Sección de ajustes
        self.steamPathLineEdit.textChanged.connect(self.ruta_steam_changed)
        self.steamGridDBKeyLineEdit.textChanged.connect(
            self.griddb_changed)
        self.lnkLocationLineEdit.textChanged.connect(self.lnk_changed)
        self.clonningModeComboBox.currentIndexChanged.connect(
            self.clonningMode_changed
        )
        self.discardRepeatedGamesCheckBox.clicked.connect(self.discard_repeats_changed)
        self.logLevelComboBox.currentIndexChanged.connect(
            self.nivel_log_changed
        )
        self.saveConfigButton.clicked.connect(self.save_config_ui)
        self.deleteExceptionButton.clicked.connect(self.remove_exception)
        
    
    #######################################
    #       Métodos de Engines
    #######################################
    def load_enginesUI(self) -> None:
        engines = self.get_engines()
        for e in engines:
            e_ui = EngineFrame(e)
            e_ui.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
            e_ui.signal_engine.connect(self.engine_selected)
            self.enginesLayout.addWidget(e_ui)
            
    def engine_selected(self, e: LauncherEngine):
        self.__prepare_gameList()
        self.stackedWidget.setCurrentWidget(self.Wgames)
        self.progressBar.setValue(0)
        self.progressBar.setFormat(f'Loading games por {e.name}:%p%')
        self.progressBar.setTextVisible(True)
        games = self.get_games(engine=e, discard=self.config.discard_repeats)
        self.__active_engine = e

        if len(games) == 0:
            RascalDialog(mensaje=f'There are no games for {e.name}.',tipo='I')
            self.stackedWidget.setCurrentWidget(self.Wwelcome)
        else:
            _actual = 1
            _total = len(games)
            for g in games:
                if self.grid_valid:
                    self.get_grid(g)
                gf = GameFrame(g,self)
                gf.signal_adding.connect(self.game_selected)
                i, j = self.__next()
                self.gamesLayout.addWidget(gf,i,j)
                self.__update_progress(_actual * 100 / _total)
                _actual += 1
            self.cacher.save_cache()
        self.progressBar.setTextVisible(False)
    
    
    #######################################
    #       Métodos de Juegos
    #######################################
    def game_selected(self, game: BasicGame):
        self.__pre_addGame(game.AppName)
        
        engine = self.__active_engine
        id = self.run_adding_game(engine=engine,game=game,mode=self.config.mode)
        if id != 0:
            if self.grid_valid:
                self.download_images(game=game,id=id)
            if self.config.mode != CLONE_SYMLINK:
                RascalDialog(mensaje="""Game added to Steam Library correctly.

NOTICE!
Important: Remember to select the desired compatibility on Steam for this game.""", tipo='I')
                self.openGameProperties(id)
            else:
                RascalDialog(mensaje="""Game added to Steam Library correctly.

NOTICE!
Important: As you selected the "CLONE_SYMLINK" mode you should select the SAME compatibility tool for this game.""", tipo='I')
                self.openGameProperties(id)
        else:
            RascalDialog(mensaje="Game NOT added to Steam Library. There are an error", tipo='E')
        self.__post_addGame()
        
        
    #######################################
    # Sección de settings
    #######################################

    def load_config_ui(self) -> None:
        self.steamPathLineEdit.setText(self.config.steam_path)
        self.steamGridDBKeyLineEdit.setText(self.config.griddb_key)
        self.lnkLocationLineEdit.setText(self.config.destination)
        if self.config.log_level == util.CRITICAL:
            self.logLevelComboBox.setCurrentIndex(0)
        elif self.config.log_level == util.ERROR:
            self.logLevelComboBox.setCurrentIndex(1)
        elif self.config.log_level == util.WARNING:
            self.logLevelComboBox.setCurrentIndex(2)
        elif self.config.log_level == util.INFO:
            self.logLevelComboBox.setCurrentIndex(3)
        else:
            self.logLevelComboBox.setCurrentIndex(4)
        self.exceptionList.clear()
        for item_text in self.config.excep:
            item = QListWidgetItem(item_text)
            self.exceptionList.addItem(item)
        if self.config.mode == CLONE_SYMLINK:
            self.clonningModeComboBox.setCurrentIndex(0)
        elif self.config.mode == CLONE_BALANCED:
            self.clonningModeComboBox.setCurrentIndex(1)
        elif self.config.mode == CLONE_FULL:
            self.clonningModeComboBox.setCurrentIndex(2)
        self.discardRepeatedGamesCheckBox.setChecked(self.config.discard_repeats)
    
    def ruta_steam_changed(self, s: str) -> None:
        config_path = s + '/config/config.vdf'
        if os.path.isfile(config_path):
            self.config.steam_path = s
        else:
            RascalDialog(mensaje=f'"{s}" is NOT a valid Steam directory',tipo='E')
            folder = self.__dialog_folder()
            new_path = folder + '/config/config.vdf'
            if os.path.isfile(new_path):
                self.steamPathLineEdit.setText(folder)
            else:
                self.steamPathLineEdit.setText(self.config.steam_path)
    
    def lnk_changed(self, s: str) -> None:
        if os.path.isdir(s):
            self.config.destination = s
        else:
            RascalDialog(mensaje=f'"{s}" is NOT a valid directory',tipo='E')
            folder = self.__dialog_folder()
            if os.path.isdir(folder):
                self.lnkLocationLineEdit.setText(folder)
            else:
                self.lnkLocationLineEdit.setText(self.config.destination)
        
    def remove_exception(self) -> None:
        excepcion = self.exceptionList.currentItem()
        if excepcion:
            self.del_exception(excepcion.text())
            index = self.exceptionList.row(excepcion)
            self.exceptionList.takeItem(index)

    def griddb_changed(self, s: str) -> None:
        self.config.griddb_key = s
    
    def clonningMode_changed(self, mode:int) -> None:
        if mode == 0:
            self.config.mode = CLONE_SYMLINK
        elif mode == 1:
            self.config.mode = CLONE_BALANCED
        elif mode == 2:
            self.config.mode = CLONE_FULL
    
    def discard_repeats_changed(self, d:bool) -> None:
        self.config.discard_repeats = d

    def nivel_log_changed(self, level: int) -> None:
        if level == 0:
            self.config.log_level = util.CRITICAL
        elif level == 1:
            self.config.log_level = util.ERROR
        elif level == 2:
            self.config.log_level = util.WARNING
        elif level == 3:
            self.config.log_level = util.INFO
        elif level == 4:
            self.config.log_level = util.DEBUG
        util.logger.setLevel(self.config.log_level)

    def save_config_ui(self) -> None:
        self.save_config()
        self.config = self.load_config()
        self.gridmanager = self.load_gridmanager()
        self.grid_valid = self.__is_grid_valid()
        RascalDialog(mensaje="Configuration saved to disk.", tipo='I')
        self.stackedWidget.setCurrentWidget(self.Wwelcome)
        
    def config_show(self) -> None:
        self.load_config_ui()
        self.stackedWidget.setCurrentWidget(self.WConfiguration)
    
    
    #######################################
    #       Métodos auxiliares
    #######################################
    def __next(self):
        _MAX_COLUMNAS = 4
        i = self.fila
        j = self.columna
        
        self.columna += 1
        if self.columna >= _MAX_COLUMNAS:
            self.fila += 1
            self.columna = 0
        return i, j
    
    def __prepare_gameList(self) -> None:
        self.__clean_WLayout(self.gamesLayout)
        self.fila = self.columna = 0
    
    def __clean_WLayout(self, layout: QVBoxLayout) -> None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
    
    def __update_progress(self, valor: int) -> None:
        self.progressBar.setValue(valor)
        if valor >= 100:
            self.progressBar.setValue(0)
        else:
            pass
    
    def __dialog_close(self) -> None:
        dialogo_pregunta = RascalDialog(
            mensaje="Do you close Rascally?", tipo='Q')
        if dialogo_pregunta.exec():
            self.save_config()
            self.close()
    
    def __is_grid_valid(self) -> bool:
        if not self.config.griddb_key:
            return False
        try:
            # Probamos a descargar TEAM FORTRESS
            if self.gridmanager.sgdb.get_game_by_steam_appid(20):
                return True
            else:
                return False
        except:
            return False
    
    def __pre_addGame(self, name: str) -> None:
        self.progressBar.setValue(0)
        hilo = threading.Thread(target=self.__loop_waiting)
        hilo.start()
        self.progressBar.setFormat(f'Adding {name} ... Please, wait!')
        self.progressBar.setTextVisible(True)
        self.setEnabled(False)
    
    def __loop_waiting(self) -> None:
        self.__loop_sem = False
        __bar = 9
        while not self.__loop_sem:
            self.progressBar.setValue(__bar)
            __bar = 9 if __bar > 90 else __bar + 10
            time.sleep(1)
        del(self.__loop_sem)
    
    def __post_addGame(self) -> None:
        self.__loop_sem = True
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)
        self.setEnabled(True)
    
    def __dialog_folder(self) -> str:
        carpeta_seleccionada = QFileDialog.getExistingDirectory(self, "Select Folder")
        return carpeta_seleccionada
        
    
    #######################################
    #       Eventos de ventana
    #######################################
    def scrollEvent(self, event: QMouseEvent):
        self.last_pos = event.position()

    def scrollMoveEvent(self, event: QMouseEvent):
        if self.last_pos is None:
            return
        delta = event.position() - self.last_pos
        self.gameArea.verticalScrollBar().setValue(self.gameArea.verticalScrollBar().value() - delta.y())
        self.last_pos = event.position()
    
    