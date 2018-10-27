# -*- coding: utf-8 -*-

"""This module provides main window for podcast app."""

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

from lubricalc.lubricalc import *
from lubricalc.config import APP_NAME
from lubricalc.config import VERSION


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
        self.central_widget = TabsGroup(self)
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


class TabsGroup(QtWidgets.QTabWidget):
    """Class to define tabs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.tabs = []
        self._add_tabs()

    def _add_tabs(self):
        for i, klass in enumerate(BaseTab.__subclasses__()):
            tab = klass()
            self.addTab(tab, '')
            self.setTabText(i, tab.text)
            # self.tabs.append(tab)


class BaseTab(QtWidgets.QWidget):
    """Base tab class."""

    def setup_ui(self):
        raise NotImplementedError('It must be implemented by subclasses')


class ViscosityIndexTab(BaseTab):
    """Class to implement viscosity index tab."""

    def __init__(self):
        super(ViscosityIndexTab, self).__init__()
        self.text = 'Viscosity Index - ASTM-D2270'
        self.setup_ui()
        self.calculate_button.clicked.connect(self.on_calculate_btn_clicked)

    def setup_ui(self):
        """Setup tab UI."""
        layout = QtWidgets.QFormLayout()
        self.v40_line_edit = QtWidgets.QLineEdit()
        self.v100_line_edit = QtWidgets.QLineEdit()
        self.vi_label = QtWidgets.QLabel('Viscosity Index Value')
        font = QtGui.QFont()
        font.setBold(True)
        self.vi_label.setFont(font)
        self.calculate_button = QtWidgets.QPushButton('Calculate')
        layout.addRow('Kinematic Viscosity at 40°C (cSt):', self.v40_line_edit)
        layout.addRow('Kinematic Viscosity at 100°C (cSt):', self.v100_line_edit)
        layout.addRow(self.calculate_button, self.vi_label)
        self.setLayout(layout)

    def on_calculate_btn_clicked(self):
        try:
            v40 = float(self.v40_line_edit.text())
            v100 = float(self.v100_line_edit.text())
        except ValueError:
            print('Enter valid data for Viscosity at 40°C and at 100°C')
            return

        if v100 > v40:
            print('Viscosity at 40°C must be greater than Viscosity at 100°C')
            return

        vi = viscosity_index_astm_d2270(v40, v100)
        self.vi_label.setText(str(vi))
