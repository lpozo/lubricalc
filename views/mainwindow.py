# -*- coding: utf-8 -*-

"""This module provides main window for Lubricalc app."""

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets

from lubricalc.config import APP_NAME
from lubricalc.config import VERSION
from .tabs import TabsCollection


class LubricalcMWin(QMainWindow):
    """Lubricalc main window."""

    def __init__(self):
        super().__init__()
        self._init_win()
        self._create_menubar()
        self._create_status_bar()

    def _init_win(self):
        self.resize(600, 600)
        self.setWindowTitle(APP_NAME + ' ' + VERSION)
        # self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(
        #     'images/multimedia-audio-player.ico')))
        self.central_widget = TabsCollection(self)
        self.central_widget.setMinimumSize(QtCore.QSize(300, 300))
        self.setCentralWidget(self.central_widget)
        self.global_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.global_layout.setContentsMargins(12, 0, 12, 0)

    def _create_menubar(self):
        menubar = QtWidgets.QMenuBar(self)
        menubar.setGeometry(QtCore.QRect(0, 0, 600, 27))
        menu_file = QtWidgets.QMenu(self.tr('&File'), menubar)
        menu_help = QtWidgets.QMenu(self.tr('&Help'), menubar)

        self.action_about = QtWidgets.QAction(self.tr('&About'), self)
        self.action_exit = QtWidgets.QAction(self.tr('&Exit'), self)

        menu_file.addAction(self.action_exit)
        menu_help.addAction(self.action_about)

        menubar.addMenu(menu_file)
        menubar.addMenu(menu_help)

        self.setMenuBar(menubar)

    def _create_status_bar(self):
        self.status_bar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.status_bar)
