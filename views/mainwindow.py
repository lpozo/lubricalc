# -*- coding: utf-8 -*-

# File name: mainwindow.py
#
# Copyright (C) 2018 Leodanis Pozo Ramos <lpozor78@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

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
