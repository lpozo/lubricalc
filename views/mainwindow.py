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


class TabsCollection(QtWidgets.QTabWidget):
    """Class to define tabs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_tabs()

    def _create_tabs(self):
        for i, klass in enumerate(BaseTab.__subclasses__()):
            tab = klass()
            self.addTab(tab, '')
            self.setTabText(i, tab.text)


class BaseTab(QtWidgets.QWidget):
    """Base tab class."""

    def setup_ui(self):
        raise NotImplementedError('It must be implemented by subclasses')


class ViscosityIndexTab(BaseTab):
    """Class to implement viscosity index tab."""

    def __init__(self):
        super().__init__()
        self.text = 'Viscosity Index'
        self.setup_ui()
        self.calculate_button.clicked.connect(self.on_calculate_btn_clicked)

    def setup_ui(self):
        """Setup tab UI."""
        font = QtGui.QFont()
        font.setBold(True)
        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(self._create_viscosity_index_group(font))
        self.setLayout(general_layout)

    def _create_viscosity_index_group(self, font):
        viscosity_index_group = QtWidgets.QGroupBox('Viscosity Index')
        viscosity_index_layout = QtWidgets.QFormLayout()
        self.v40_line_edit = QtWidgets.QLineEdit()
        self.v100_line_edit = QtWidgets.QLineEdit()
        self.vi_label = QtWidgets.QLabel('Viscosity Index')
        self.vi_label.setFont(font)
        self.calculate_button = QtWidgets.QPushButton('Calculate')
        viscosity_index_layout.addRow('Kinematic Viscosity at 40°C (cSt):',
                                      self.v40_line_edit)
        viscosity_index_layout.addRow('Kinematic Viscosity at 100°C (cSt):',
                                      self.v100_line_edit)
        viscosity_index_layout.addRow(self.calculate_button, self.vi_label)
        viscosity_index_group.setLayout(viscosity_index_layout)

        return viscosity_index_group

    def on_calculate_btn_clicked(self):
        try:
            vi = viscosity_index(KV40=self.v40_line_edit.text(),
                                 KV100=self.v100_line_edit.text())
            self.vi_label.setText('Viscosity Index = ' + str(vi))
        except ValueError:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  'Enter valid data for Viscosity'
                                  ' at 40°C and at 100°C',
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except ConceptError:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  'Viscosity at 40°C must be'
                                  ' greater than Viscosity at 100°C',
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()


class BaseOilMixtureTab(BaseTab):
    """Class to implement Base Oil Mixture tab."""

    def __init__(self):
        super().__init__()
        self.text = 'Base Oil Mixture'
        self.setup_ui()
        self.calculate_viscosity_button.clicked.connect(
            self.on_calculate_viscosity_btn_clicked)
        self.calculate_proportions_button.clicked.connect(
            self.on_calculate_proportions_btn_clicked)

    def setup_ui(self):
        """Setup tab UI."""
        font = QtGui.QFont()
        font.setBold(True)
        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(self._create_base_oil_mixture_group(font))
        general_layout.addWidget(self._create_base_oil_proportions_group(font))
        self.setLayout(general_layout)

    def _create_base_oil_mixture_group(self, font):
        base_oil_mixture_group = QtWidgets.QGroupBox(
            'Mixture Kinematic Viscosity')
        base_oil_mixture_layout = QtWidgets.QFormLayout()
        self.KV1_line_edit = QtWidgets.QLineEdit()
        self.KV2_line_edit = QtWidgets.QLineEdit()
        self.oil1_percent_line_edit = QtWidgets.QLineEdit()
        self.temperature_combo = QtWidgets.QComboBox()
        self.temperature_combo.addItems(('100', '40', '-5'))
        self.mix_KV_label = QtWidgets.QLabel('Mixture Kinematic Viscosity')
        self.mix_KV_label.setFont(font)
        self.calculate_viscosity_button = QtWidgets.QPushButton('Calculate')
        base_oil_mixture_layout.addRow(
            '1st Base Oil Kinematic Viscosity (cSt):',
            self.KV1_line_edit)
        base_oil_mixture_layout.addRow(
            '2nd Base Oil Kinematic Viscosity (cSt):',
            self.KV2_line_edit)
        base_oil_mixture_layout.addRow(
            '1st Base Oil Proportion in Mixture (%):',
            self.oil1_percent_line_edit)
        base_oil_mixture_layout.addRow('Temperature (°C):',
                                       self.temperature_combo)
        base_oil_mixture_layout.addRow(self.calculate_viscosity_button,
                                       self.mix_KV_label)
        base_oil_mixture_group.setLayout(base_oil_mixture_layout)

        return base_oil_mixture_group

    def _create_base_oil_proportions_group(self, font):
        base_oil_proportions_group = QtWidgets.QGroupBox('Mixture Proportions')
        base_oil_proportions_layout = QtWidgets.QFormLayout()
        self.KV1_line_edit = QtWidgets.QLineEdit()
        self.KV2_line_edit = QtWidgets.QLineEdit()
        self.KV_line_edit = QtWidgets.QLineEdit()
        self.temperature_combo = QtWidgets.QComboBox()
        self.temperature_combo.addItems(('100', '40', '-5'))
        self.oil1_line_edit = QtWidgets.QLineEdit()
        self.oil2_line_edit = QtWidgets.QLineEdit()
        self.oil1_label = QtWidgets.QLabel('1st Oil Proportion in Mixture (%)')
        self.oil2_label = QtWidgets.QLabel('2nd Oil Proportion in Mixture (%)')
        self.oil1_label.setFont(font)
        self.oil2_label.setFont(font)
        self.calculate_proportions_button = QtWidgets.QPushButton('Calculate')
        base_oil_proportions_layout.addRow(
            '1st Base Oil Kinematic Viscosity (cSt):',
            self.KV1_line_edit)
        base_oil_proportions_layout.addRow(
            '2nd Base Oil Kinematic Viscosity (cSt):',
            self.KV2_line_edit)
        base_oil_proportions_layout.addRow(
            'Mixture Kinematic Viscosity (cSt):',
            self.KV_line_edit)
        base_oil_proportions_layout.addRow('Temperature (°C):',
                                           self.temperature_combo)

        base_oil_proportions_layout.addRow(self.calculate_proportions_button,
                                           self.oil1_label)
        base_oil_proportions_layout.addRow(QtWidgets.QWidget(),
                                           self.oil2_label)
        base_oil_proportions_group.setLayout(base_oil_proportions_layout)

        return base_oil_proportions_group

    def on_calculate_viscosity_btn_clicked(self):
        mix_KV = OilMixture().oil_mix(
            KV1=self.KV1_line_edit.text(),
            KV2=self.KV2_line_edit.text(),
            oil1_percent=self.oil1_percent_line_edit.text(),
            temperature=self.temperature_combo.currentText())
        self.mix_KV_label.setText('Mixture Kinematic Viscosity' + ' = ' +
                                  str(mix_KV) + ' ' + 'cSt')

    def on_calculate_proportions_btn_clicked(self):
        proportions = OilMixture().mix_proportions(
            KV=self.KV_line_edit.text(),
            KV1=self.KV1_line_edit.text(),
            KV2=self.KV2_line_edit.text(),
            temperature=self.temperature_combo.currentText())
        self.oil1_label.setText('1st Oil Proportion in Mixture' + ' = ' +
                                str(proportions[0]) + ' ' + '%')
        self.oil2_label.setText('2nd Oil Proportion in Mixture' + ' = ' +
                                str(proportions[1]) + ' ' + '%')


class SulfatedAshTab(BaseTab):
    """Class to implement Sulfated ash tab."""

    def __init__(self):
        super().__init__()
        self.text = 'Total Sulfated Ash'
        self.setup_ui()
        self.additive_button.clicked.connect(self.on_additive_btn_clicked)
        self.total_ash_button.clicked.connect(self.on_total_ash_btn_clicked)

    def setup_ui(self):
        """Setup tab UI."""
        font = QtGui.QFont()
        font.setBold(True)
        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(self._create_additive_group(font))
        general_layout.addWidget(self._create_sulfated_ash_group(font))
        self.setLayout(general_layout)

    def _create_additive_group(self, font):
        additive_group = QtWidgets.QGroupBox('Additive (% mass)')
        additive_layout = QtWidgets.QFormLayout()
        additive_group.setLayout(additive_layout)
        self.additive_percent = QtWidgets.QLineEdit()
        additive_layout.addRow('Total Additive (% mass):',
                               self.additive_percent)
        self.additive_density = QtWidgets.QLineEdit()
        additive_layout.addRow('Additive Density (kg/L):',
                               self.additive_density)
        self.oil_density = QtWidgets.QLineEdit()
        additive_layout.addRow('Density of Finished Oil (kg/L):',
                               self.oil_density)
        self.additive_button = QtWidgets.QPushButton('Calculate')
        self.additive_label = QtWidgets.QLabel('Additive (% mass)')
        self.additive_label.setFont(font)
        additive_layout.addRow(self.additive_button, self.additive_label)
        return additive_group

    def _create_sulfated_ash_group(self, font):
        sulfated_ash_group = QtWidgets.QGroupBox('Total Sulfated Ash')
        sulfated_ash_layout = QtWidgets.QFormLayout()
        sulfated_ash_group.setLayout(sulfated_ash_layout)
        self.additive_percent = QtWidgets.QLineEdit()
        sulfated_ash_layout.addRow('Total Additive (% mass):',
                               self.additive_percent)

        for metal in OilBlend().metals:
            line_edit = QtWidgets.QLineEdit()
            line_edit.setText('0')
            self.__dict__[metal] = line_edit
            sulfated_ash_layout.addRow(metal.capitalize() + ' (% mass):',
                                       line_edit)
        self.total_ash_button = QtWidgets.QPushButton('Calculate')
        self.total_ash_label = QtWidgets.QLabel('Total Sulfated Ash (% mass)')
        self.total_ash_label.setFont(font)
        sulfated_ash_layout.addRow(self.total_ash_button, self.total_ash_label)

        return sulfated_ash_group

    def on_additive_btn_clicked(self):
        blend = OilBlend(additive_percent=float(self.additive_percent.text()))
        additive = blend.additive_percent_mass(
            additive_density=float(self.additive_density.text()),
            final_oil_density=float(self.oil_density.text()))
        self.additive_label.setText('Additive (% mass)' + ' = ' +
                                    str(additive) + ' ' + '%')

    def on_total_ash_btn_clicked(self):
        blend = OilBlend(additive_percent=float(self.additive_percent.text()))
        metal_contents = {}
        for metal in blend.metals:
            metal_contents[metal] = float(self.__dict__[metal].text())

        total_ash = blend.total_ash(**metal_contents)
        self.total_ash_label.setText('Total Sulfated Ash (% mass)' + ' = ' +
                                     str(total_ash) + ' %')


class BearingTab(BaseTab):
    """Class to implement Bearing Lubrication tab."""

    def __init__(self):
        super().__init__()
        self.text = 'Bearing Lubrication'
        self.setup_ui()
        self.grease_amount_button.clicked.connect(
            self.on_grease_amount_btn_clicked)
        self.frequency_button.clicked.connect(self.on_frequency_btn_clicked)

    def setup_ui(self):
        """Setup tab UI."""
        font = QtGui.QFont()
        font.setBold(True)
        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(self._create_params_group())
        general_layout.addWidget(self._create_grease_amount_group(font))
        general_layout.addWidget(self._create_frequency_group(font))
        self.setLayout(general_layout)

    def _create_params_group(self):
        params_group = QtWidgets.QGroupBox('Bearing Parameters')
        params_layout = QtWidgets.QFormLayout()
        params_group.setLayout(params_layout)
        self.D_line_edit = QtWidgets.QLineEdit()
        self.d_line_edit = QtWidgets.QLineEdit()
        self.B_line_edit = QtWidgets.QLineEdit()
        self.temperature_line_edit = QtWidgets.QLineEdit()
        self.rpm_line_edit = QtWidgets.QLineEdit()
        params_layout.addRow('Outer Diameter (mm):', self.D_line_edit)
        params_layout.addRow('Inner Diameter (mm):', self.d_line_edit)
        params_layout.addRow('Total Width (mm):', self.B_line_edit)
        params_layout.addRow('Rotation Speed (rpm):', self.rpm_line_edit)
        params_layout.addRow('Operation Temperature (°C):',
                             self.temperature_line_edit)
        return params_group

    def _create_grease_amount_group(self, font):
        grease_amount_group = QtWidgets.QGroupBox(
            'Amount of Grease for Re-lubrication')
        grease_amount_layout = QtWidgets.QFormLayout()
        self.grease_amount_button = QtWidgets.QPushButton('Calculate')
        self.grease_amount_label = QtWidgets.QLabel(
            'Amount of Grease for Re-lubrication')
        self.grease_amount_label.setFont(font)
        grease_amount_layout.addRow(self.grease_amount_button,
                                    self.grease_amount_label)
        grease_amount_group.setLayout(grease_amount_layout)
        return grease_amount_group

    def _create_frequency_group(self, font):
        frequency_group = QtWidgets.QGroupBox('Re-lubrication Frequency')
        frequency_layout = QtWidgets.QFormLayout()
        frequency_group.setLayout(frequency_layout)
        self.frequency_button = QtWidgets.QPushButton('Calculate')
        self.frequency_label = QtWidgets.QLabel('Re-lubrication Frequency')
        self.frequency_label.setFont(font)
        self.Fc = QtWidgets.QComboBox()
        frequency_layout.addRow('Contamination Factor:', self.Fc)
        self.Fc.addItems(('Light, no abrasive dust',
                          'Severe, no abrasive dust',
                          'Light, abrasive dust',
                          'Severe, abrasive dust'))

        self.Fh = QtWidgets.QComboBox()
        frequency_layout.addRow('Humidity Factor:', self.Fh)
        self.Fh.addItems(('Relative Humidity < 80 %',
                          'Relative Humidity from 80 to 90 %',
                          'Occasional condensation',
                          'Water Presence'))

        self.Fv = QtWidgets.QComboBox()
        frequency_layout.addRow('Vibration Factor:', self.Fv)
        self.Fv.addItems(('Top speed < 0.2 ips',
                          'Top speed from 0.2 to 0.4 ips',
                          'Top speed > 0.4 ips'))

        self.Fp = QtWidgets.QComboBox()
        frequency_layout.addRow('Position Factor:', self.Fp)
        self.Fp.addItems(('Horizontal',
                          '45 Degrees',
                          'Vertical'))

        self.Fd = QtWidgets.QComboBox()
        frequency_layout.addRow('Design Factor:', self.Fd)
        self.Fd.addItems(('Ball bearing',
                          'Cylinder/Needle roller bearing',
                          'Conical roller bearing'))

        frequency_layout.addRow(self.frequency_button, self.frequency_label)

        return frequency_group

    def on_grease_amount_btn_clicked(self):
        bearing = Bearing(D=float(self.D_line_edit.text()),
                          d=float(self.d_line_edit.text()),
                          B=float(self.B_line_edit.text()),
                          temperature=float(self.temperature_line_edit.text()),
                          rpm=float(self.rpm_line_edit.text()))
        self.grease_amount_label.setText('Amount of Grease for Re-lubrication'
                                         + ' = ' +
                                         str(bearing.grease_amount())
                                         + ' ' +
                                         'g')

    def on_frequency_btn_clicked(self):
        bearing = Bearing(D=float(self.D_line_edit.text()),
                          d=float(self.d_line_edit.text()),
                          B=float(self.B_line_edit.text()),
                          temperature=float(self.temperature_line_edit.text()),
                          rpm=float(self.rpm_line_edit.text()))
        self.frequency_label.setText('Re-lubrication Frequency'
                                     + ' = ' +
                                     str(bearing.lubrication_frequency(
                                         contamination=self.Fc.currentIndex(),
                                         moisture=self.Fh.currentIndex(),
                                         vibration=self.Fv.currentIndex(),
                                         position=self.Fp.currentIndex(),
                                         design=self.Fd.currentIndex()))
                                     + ' ' +
                                     'hours')
