# -*- coding: utf-8 -*-

# File name: controller.py
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

"""This module provides Main Controller."""

import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from views.mainwindow import LubricalcMWin
from lubricalc.config import APP_NAME
from lubricalc.config import LONG_DESC
from lubricalc.lubricalc import *


class MainController:
    """Class to provide main controller."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.model = None
        self.view = LubricalcMWin()
        self._connect_events()

    def run(self):
        self.view.show()
        sys.exit(self.app.exec_())

    def _connect_events(self):
        self.view.action_exit.triggered.connect(self.on_exit_triggered)
        self.view.action_about.triggered.connect(self.on_about_triggered)

    def on_exit_triggered(self):
        self.app.quit()

    def on_about_triggered(self):
        QMessageBox.about(self.view.central_widget,
                          self.view.tr('About') + ' ' + APP_NAME,
                          LONG_DESC)
