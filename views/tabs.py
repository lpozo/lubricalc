# -*- coding: utf-8 -*-

# File name: tabs.py
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

"""This module provides Tabs for Lubricalc app."""

from PyQt5 import QtGui, QtWidgets

from lubricalc.reynolds import *


class TabsCollection(QtWidgets.QTabWidget):
    """Class to define tabs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_tabs()

    def _create_tabs(self):
        for tab_class in BaseTab.__subclasses__():
            tab = tab_class()
            self.addTab(tab, tab.text)


class BaseTab(QtWidgets.QWidget):
    """Base tab class."""

    def __init__(self):
        super().__init__()
        self.font = QtGui.QFont()
        self.font.setBold(True)

    def setup_ui(self):
        raise NotImplementedError('It must be implemented by subclasses')


class ViscosityTab(BaseTab):
    """Class to implement Viscosity tab."""

    def __init__(self):
        super().__init__()
        self.text = 'Viscosity'
        self.setup_ui()
        self.viscosity_index_btn.clicked.connect(
            self.on_viscosity_index_button_clicked)
        self.viscosity_40_btn.clicked.connect(
            self.on_viscosity_at_40_button_clicked)
        self.viscosity_100_btn.clicked.connect(
            self.on_calculate_viscosity_at_100_btn_clicked)

    def setup_ui(self):
        """Setup tab UI."""
        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(self._create_viscosity_index_group())
        general_layout.addWidget(self._create_viscosity_at_40_group())
        general_layout.addWidget(self._create_viscosity_at_100_group())
        self.setLayout(general_layout)

    def _create_viscosity_index_group(self):
        index_gpb = QtWidgets.QGroupBox('Viscosity Index')
        index_layout = QtWidgets.QFormLayout()
        self.viscosity0_40_edit = QtWidgets.QLineEdit()
        self.viscosity0_100_edit = QtWidgets.QLineEdit()
        self.index_label = QtWidgets.QLabel('Viscosity Index')
        self.index_label.setFont(self.font)
        self.viscosity_index_btn = QtWidgets.QPushButton('Calculate')
        index_layout.addRow('Kinematic Viscosity at 40°C (cSt):',
                            self.viscosity0_40_edit)
        index_layout.addRow('Kinematic Viscosity at 100°C (cSt):',
                            self.viscosity0_100_edit)
        index_layout.addRow(self.viscosity_index_btn, self.index_label)
        index_gpb.setLayout(index_layout)
        self.index_label.setToolTip(viscosity_index.__doc__)
        return index_gpb

    def _create_viscosity_at_40_group(self):
        viscosity_40_gpb = QtWidgets.QGroupBox('Kinematic Viscosity at 40°C')
        viscosity_40_layout = QtWidgets.QFormLayout()
        self.viscosity1_100_edit = QtWidgets.QLineEdit()
        self.index0_edit = QtWidgets.QLineEdit()
        self.viscosity_40_label = QtWidgets.QLabel(
            'Kinematic Viscosity at 40°C')
        self.viscosity_40_label.setFont(self.font)
        self.viscosity_40_btn = QtWidgets.QPushButton('Calculate')
        viscosity_40_layout.addRow('Kinematic Viscosity at 100°C (cSt):',
                                   self.viscosity1_100_edit)
        viscosity_40_layout.addRow('Viscosity Index:',
                                   self.index0_edit)
        viscosity_40_layout.addRow(self.viscosity_40_btn,
                                   self.viscosity_40_label)
        viscosity_40_gpb.setLayout(viscosity_40_layout)
        return viscosity_40_gpb

    def _create_viscosity_at_100_group(self):
        viscosity_100_gpb = QtWidgets.QGroupBox('Kinematic Viscosity at 100°C')
        viscosity_100_layout = QtWidgets.QFormLayout()
        self.viscosity1_40_edit = QtWidgets.QLineEdit()
        self.index1_edit = QtWidgets.QLineEdit()
        self.viscosity_100_label = QtWidgets.QLabel(
            'Kinematic Viscosity at 100°C')
        self.viscosity_100_label.setFont(self.font)
        self.viscosity_100_btn = QtWidgets.QPushButton('Calculate')
        viscosity_100_layout.addRow('Kinematic Viscosity at 40°C (cSt):',
                                    self.viscosity1_40_edit)
        viscosity_100_layout.addRow('Viscosity Index:',
                                    self.index1_edit)
        viscosity_100_layout.addRow(self.viscosity_100_btn,
                                    self.viscosity_100_label)
        viscosity_100_gpb.setLayout(viscosity_100_layout)
        return viscosity_100_gpb

    def on_viscosity_index_button_clicked(self):
        try:
            vi = viscosity_index(viscosity_40=self.viscosity0_40_edit.text(),
                                 viscosity_100=self.viscosity0_100_edit.text())
            self.index_label.setText('Viscosity Index = ' + str(vi))
        except ValueError:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  'Enter valid data for Viscosity'
                                  ' at 40°C and at 100°C',
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except InvertedViscosityError:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  'Viscosity at 40°C must be'
                                  ' greater than Viscosity at 100°C',
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except TooLowViscosityError:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  'Viscosity must be greater than 2',
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()

    def on_viscosity_at_40_button_clicked(self):
        try:
            result = viscosity_at_40(
                viscosity_100=self.viscosity1_100_edit.text(),
                v_index=self.index0_edit.text())
            self.viscosity_40_label.setText('Kinematic Viscosity at 40°C' +
                                            ' = ' + str(result) + ' ' + 'cSt')
        except (ValueError, ConceptError):
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  'Enter valid data for Viscosity at 100°C '
                                  'and Viscosity Index',
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except TooLowViscosityError:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  'Viscosity must be greater than 2',
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()

    def on_calculate_viscosity_at_100_btn_clicked(self):
        try:
            result = viscosity_at_100(
                viscosity_40=self.viscosity1_40_edit.text(),
                v_index=self.index1_edit.text())
            self.viscosity_100_label.setText('Kinematic Viscosity at 100°C' +
                                             ' = ' + str(result) + ' ' + 'cSt')
        except ValueError:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  'Enter valid data for Viscosity at 40°C '
                                  'and Viscosity Index',
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except TooLowViscosityError:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  'Viscosity must be greater than 2',
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
        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(self._create_base_oil_mixture_group())
        general_layout.addWidget(self._create_base_oil_proportions_group())
        self.setLayout(general_layout)

    def _create_base_oil_mixture_group(self):
        base_oil_mixture_group = QtWidgets.QGroupBox(
            'Mixture Kinematic Viscosity')
        base_oil_mixture_layout = QtWidgets.QFormLayout()
        self.KV1_line_edit = QtWidgets.QLineEdit()
        self.KV2_line_edit = QtWidgets.QLineEdit()
        self.oil1_percent_line_edit = QtWidgets.QLineEdit()
        self.temperature_combo = QtWidgets.QComboBox()
        self.temperature_combo.addItems(('100', '40', '-5'))
        self.mix_KV_label = QtWidgets.QLabel('Mixture Kinematic Viscosity')
        self.mix_KV_label.setFont(self.font)
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

    def _create_base_oil_proportions_group(self):
        base_oil_proportions_group = QtWidgets.QGroupBox('Mixture Proportions')
        base_oil_proportions_layout = QtWidgets.QFormLayout()
        self.KV1_line_edit = QtWidgets.QLineEdit()
        self.KV2_line_edit = QtWidgets.QLineEdit()
        self.KV_line_edit = QtWidgets.QLineEdit()
        self.temperature_combo = QtWidgets.QComboBox()
        self.temperature_combo.addItems(('100', '40', '-5'))
        self.oil1_line_edit = QtWidgets.QLineEdit()
        self.oil2_line_edit = QtWidgets.QLineEdit()
        self.oil1_label = QtWidgets.QLabel('1st Oil Proportion in Mixture')
        self.oil2_label = QtWidgets.QLabel('2nd Oil Proportion in Mixture')
        self.oil1_label.setFont(self.font)
        self.oil2_label.setFont(self.font)
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
        mix_KV = OilMixture().oil_mix_viscosity(
            viscosity0=self.KV1_line_edit.text(),
            viscosity1=self.KV2_line_edit.text(),
            oil0_percent=self.oil1_percent_line_edit.text(),
            temperature=self.temperature_combo.currentText())
        self.mix_KV_label.setText('Mixture Kinematic Viscosity' + ' = ' +
                                  str(mix_KV) + ' ' + 'cSt')

    def on_calculate_proportions_btn_clicked(self):
        proportions = OilMixture().mix_proportions(
            viscosity0=self.KV_line_edit.text(),
            viscosity1=self.KV1_line_edit.text(),
            mix_viscosity=self.KV2_line_edit.text(),
            temperature=self.temperature_combo.currentText())
        self.oil1_label.setText('1st Oil Proportion in Mixture' + ' = ' +
                                str(proportions[0]) + ' ' + '%')
        self.oil2_label.setText('2nd Oil Proportion in Mixture' + ' = ' +
                                str(proportions[1]) + ' ' + '%')


class SulfatedAshTab(BaseTab):
    """Class to implement Sulfated ash tab."""

    def __init__(self):
        super().__init__()
        self.text = 'Total Ash'
        self.setup_ui()
        self.additive_btn.clicked.connect(self.on_additive_btn_clicked)
        self.total_ash_btn.clicked.connect(self.on_total_ash_btn_clicked)

    def setup_ui(self):
        """Setup tab UI."""
        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(self._create_additive_group())
        general_layout.addWidget(self._create_ash_group())
        self.setLayout(general_layout)

    def _create_additive_group(self):
        additive_gpb = QtWidgets.QGroupBox('Additive')
        additive_layout = QtWidgets.QFormLayout()
        additive_gpb.setLayout(additive_layout)
        self.additive_percent0_edit = QtWidgets.QLineEdit()
        additive_layout.addRow('Total Additive (% by mass):',
                               self.additive_percent0_edit)
        self.additive_density_edit = QtWidgets.QLineEdit()
        additive_layout.addRow('Additive Density (kg/L):',
                               self.additive_density_edit)
        self.oil_density_edit = QtWidgets.QLineEdit()
        additive_layout.addRow('Density of Finished Oil (kg/L):',
                               self.oil_density_edit)
        self.additive_btn = QtWidgets.QPushButton('Calculate')
        self.additive_label = QtWidgets.QLabel('Additive')
        self.additive_label.setFont(self.font)
        additive_layout.addRow(self.additive_btn, self.additive_label)
        return additive_gpb

    def _create_ash_group(self):
        ash_gpb = QtWidgets.QGroupBox('Total Ash')
        ash_layout = QtWidgets.QFormLayout()
        ash_gpb.setLayout(ash_layout)
        self.additive_percent1_edit = QtWidgets.QLineEdit()
        ash_layout.addRow('Total Additive (% by mass):',
                          self.additive_percent1_edit)

        for metal in OilBlend.metals():
            edit = QtWidgets.QLineEdit()
            edit.setText('0')
            self.__dict__[metal] = edit
            ash_layout.addRow(metal.capitalize() + ' (% by mass):', edit)

        self.total_ash_btn = QtWidgets.QPushButton('Calculate')
        self.total_ash_label = QtWidgets.QLabel('Total Ash')
        self.total_ash_label.setFont(self.font)
        ash_layout.addRow(self.total_ash_btn, self.total_ash_label)

        return ash_gpb

    def on_additive_btn_clicked(self):
        blend = OilBlend(additive_percent=self.additive_percent0_edit.text())
        additive = blend.additive_percent_mass(
            additive_density=self.additive_density_edit.text(),
            final_oil_density=self.oil_density_edit.text())
        self.additive_label.setText('Additive' + ' = ' +
                                    str(additive) + ' ' + '% by mass')

    def on_total_ash_btn_clicked(self):
        blend = OilBlend(additive_percent=self.additive_percent1_edit.text())
        metal_contents = {}
        for metal in OilBlend.metals():
            metal_contents[metal] = float(self.__dict__[metal].text())

        total_ash = blend.total_ash(**metal_contents)
        self.total_ash_label.setText('Total Ash' + ' = ' + str(total_ash) +
                                     ' % by mass')


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
        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(self._create_grease_amount_group())
        general_layout.addWidget(self._create_frequency_group())
        self.setLayout(general_layout)

    def _create_grease_amount_group(self):
        grease_amount_group = QtWidgets.QGroupBox(
            'Amount of Grease for Re-lubrication')
        grease_amount_layout = QtWidgets.QFormLayout()
        self.D_line_edit = QtWidgets.QLineEdit()
        self.B_line_edit = QtWidgets.QLineEdit()
        self.grease_amount_button = QtWidgets.QPushButton('Calculate')
        self.grease_amount_label = QtWidgets.QLabel(
            'Amount of Grease for Re-lubrication')
        self.grease_amount_label.setFont(self.font)
        grease_amount_layout.addRow('Outer Diameter (mm):', self.D_line_edit)
        grease_amount_layout.addRow('Total Width (mm):', self.B_line_edit)
        grease_amount_layout.addRow(self.grease_amount_button,
                                    self.grease_amount_label)
        grease_amount_group.setLayout(grease_amount_layout)
        return grease_amount_group

    def _create_frequency_group(self):
        frequency_group = QtWidgets.QGroupBox('Re-lubrication Frequency')
        frequency_layout = QtWidgets.QFormLayout()
        frequency_group.setLayout(frequency_layout)
        self.frequency_button = QtWidgets.QPushButton('Calculate')
        self.frequency_label = QtWidgets.QLabel('Re-lubrication Frequency')
        self.frequency_label.setFont(self.font)
        self.rpm1_line_edit = QtWidgets.QLineEdit()
        frequency_layout.addRow('Rotation Speed (rpm):', self.rpm1_line_edit)
        self.d1_line_edit = QtWidgets.QLineEdit()
        frequency_layout.addRow('Inner Diameter (mm):', self.d1_line_edit)
        self.Ft = QtWidgets.QComboBox()
        frequency_layout.addRow('Temperature:', self.Ft)
        self.Ft.addItems(('< 65°C',
                          '65 to 80°C',
                          '80 to 93°C',
                          '> 93°C',))
        self.Fc = QtWidgets.QComboBox()
        frequency_layout.addRow('Contamination:', self.Fc)
        self.Fc.addItems(('Light, no abrasive dust',
                          'Severe, no abrasive dust',
                          'Light, abrasive dust',
                          'Severe, abrasive dust'))

        self.Fh = QtWidgets.QComboBox()
        frequency_layout.addRow('Humidity:', self.Fh)
        self.Fh.addItems(('Relative Humidity < 80 %',
                          'Relative Humidity from 80 to 90 %',
                          'Occasional condensation',
                          'Water Presence'))

        self.Fv = QtWidgets.QComboBox()
        frequency_layout.addRow('Vibration:', self.Fv)
        self.Fv.addItems(('Top speed < 0.5 cm/s',
                          'Top speed from 0.5 to 1.0 cm/s',
                          'Top speed > 1.0 cm/s'))

        self.Fp = QtWidgets.QComboBox()
        frequency_layout.addRow('Position:', self.Fp)
        self.Fp.addItems(('Horizontal',
                          '45 Degrees',
                          'Vertical'))

        self.Fd = QtWidgets.QComboBox()
        frequency_layout.addRow('Bearing Design:', self.Fd)
        self.Fd.addItems(('Ball bearing',
                          'Cylinder/Needle roller bearing',
                          'Conical roller bearing'))

        frequency_layout.addRow(self.frequency_button, self.frequency_label)

        return frequency_group

    def on_grease_amount_btn_clicked(self):
        grease_amount = Bearing.grease_amount(
            outer_diameter=self.D_line_edit.text(),
            width=self.B_line_edit.text())
        self.grease_amount_label.setText('Amount of Grease for Re-lubrication'
                                         + ' = ' + str(grease_amount)
                                         + ' ' + 'g')

    def on_frequency_btn_clicked(self):
        frequency = Bearing.lubrication_frequency(
            rpm=self.rpm1_line_edit.text(),
            inner_diameter=self.d1_line_edit.text(),
            ft=self.Ft.currentIndex(),
            fh=self.Fh.currentIndex(),
            fv=self.Fv.currentIndex(),
            fp=self.Fp.currentIndex(),
            fc=self.Fc.currentIndex(),
            fd=self.Fd.currentIndex())
        self.frequency_label.setText('Re-lubrication Frequency' + ' = ' +
                                     str(frequency) + ' ' + 'hours')
