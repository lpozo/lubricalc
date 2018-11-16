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

from lubricalc.blend import OilBlend
from lubricalc.exception import *
from lubricalc.bearing import Bearing
from lubricalc.mixture import OilMixture
from lubricalc.viscosity import Viscosity


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
            self.on_viscosity_40_button_clicked)
        self.viscosity_100_btn.clicked.connect(
            self.on_viscosity_100_button_clicked)

    def setup_ui(self):
        """Setup tab UI."""
        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(self._create_viscosity_index_group())
        general_layout.addWidget(self._create_viscosity_40_group())
        general_layout.addWidget(self._create_viscosity_100_group())
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
        self.viscosity_index_btn.setToolTip(
            Viscosity().viscosity_index.__doc__)
        return index_gpb

    def _create_viscosity_40_group(self):
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
        self.viscosity_40_btn.setToolTip(Viscosity().viscosity_at_40.__doc__)
        return viscosity_40_gpb

    def _create_viscosity_100_group(self):
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
        self.viscosity_100_btn.setToolTip(Viscosity().viscosity_at_100.__doc__)
        return viscosity_100_gpb

    def on_viscosity_index_button_clicked(self):
        try:
            vi = Viscosity().viscosity_index(
                viscosity40=self.viscosity0_40_edit.text(),
                viscosity100=self.viscosity0_100_edit.text())
            self.index_label.setText('Viscosity Index' + ' = ' + str(vi))
        except ValueError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except InvertedViscosityError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except ConceptError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()

    def on_viscosity_40_button_clicked(self):
        try:
            result = Viscosity().viscosity_at_40(
                viscosity100=self.viscosity1_100_edit.text(),
                v_index=self.index0_edit.text())
            self.viscosity_40_label.setText('Kinematic Viscosity at 40°C' +
                                            ' = ' + str(result) + ' ' + 'cSt')
        except ValueError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except ConceptError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()

    def on_viscosity_100_button_clicked(self):
        try:
            result = Viscosity().viscosity_at_100(
                viscosity40=self.viscosity1_40_edit.text(),
                v_index=self.index1_edit.text())
            self.viscosity_100_label.setText('Kinematic Viscosity at 100°C' +
                                             ' = ' + str(result) + ' ' + 'cSt')
        except ValueError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except ConceptError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()


class BaseOilMixtureTab(BaseTab):
    """Class to implement Base Oil Mixture tab."""

    def __init__(self):
        super().__init__()
        self.text = 'Oil Mixture'
        self.setup_ui()
        self.mix_viscosity_btn.clicked.connect(
            self.on_mix_viscosity_button_clicked)
        self.mix_proportions_btn.clicked.connect(
            self.on_calculate_proportions_btn_clicked)

    def setup_ui(self):
        """Setup tab UI."""
        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(self._create_base_oil_mixture_group())
        general_layout.addWidget(self._create_base_oil_proportions_group())
        self.setLayout(general_layout)

    def _create_base_oil_mixture_group(self):
        oil_mixture_gpb = QtWidgets.QGroupBox('Mixture Kinematic Viscosity')
        oil_mixture_layout = QtWidgets.QFormLayout()
        self.viscosity01_edit = QtWidgets.QLineEdit()
        self.viscosity02_edit = QtWidgets.QLineEdit()
        self.oil1_percent_edit = QtWidgets.QLineEdit()
        self.temperature0_combo = QtWidgets.QComboBox()
        self.temperature0_combo.addItems(('100', '40', '-5'))
        self.mix_viscosity_label = QtWidgets.QLabel(
            'Mixture Kinematic Viscosity')
        self.mix_viscosity_label.setFont(self.font)
        self.mix_viscosity_btn = QtWidgets.QPushButton('Calculate')
        oil_mixture_layout.addRow('1st. Base Oil Kinematic Viscosity (cSt):',
                                  self.viscosity01_edit)
        oil_mixture_layout.addRow('2nd. Base Oil Kinematic Viscosity (cSt):',
                                  self.viscosity02_edit)
        oil_mixture_layout.addRow('1st. Base Oil Proportion in Mixture (%):',
                                  self.oil1_percent_edit)
        oil_mixture_layout.addRow('Temperature (°C):', self.temperature0_combo)
        oil_mixture_layout.addRow(self.mix_viscosity_btn,
                                  self.mix_viscosity_label)
        oil_mixture_gpb.setLayout(oil_mixture_layout)

        return oil_mixture_gpb

    def _create_base_oil_proportions_group(self):
        proportions_gpb = QtWidgets.QGroupBox('Mixture Proportions')
        proportions_layout = QtWidgets.QFormLayout()
        self.viscosity11_edit = QtWidgets.QLineEdit()
        self.viscosity12_edit = QtWidgets.QLineEdit()
        self.mix_viscosity_edit = QtWidgets.QLineEdit()
        self.temperature1_combo = QtWidgets.QComboBox()
        self.temperature1_combo.addItems(('100', '40', '-5'))
        self.oil1_edit = QtWidgets.QLineEdit()
        self.oil2_edit = QtWidgets.QLineEdit()
        self.oil1_label = QtWidgets.QLabel('1st. Oil Proportion in Mixture')
        self.oil2_label = QtWidgets.QLabel('2nd. Oil Proportion in Mixture')
        self.oil1_label.setFont(self.font)
        self.oil2_label.setFont(self.font)
        self.mix_proportions_btn = QtWidgets.QPushButton('Calculate')
        proportions_layout.addRow('1st. Base Oil Kinematic Viscosity (cSt):',
                                  self.viscosity11_edit)
        proportions_layout.addRow('2nd. Base Oil Kinematic Viscosity (cSt):',
                                  self.viscosity12_edit)
        proportions_layout.addRow('Mixture Kinematic Viscosity (cSt):',
                                  self.mix_viscosity_edit)
        proportions_layout.addRow('Temperature (°C):', self.temperature1_combo)
        proportions_layout.addRow(self.mix_proportions_btn, self.oil1_label)
        proportions_layout.addRow(QtWidgets.QWidget(), self.oil2_label)
        proportions_gpb.setLayout(proportions_layout)

        return proportions_gpb

    def on_mix_viscosity_button_clicked(self):
        try:
            mix_viscosity = OilMixture().oil_mix_viscosity(
                viscosity0=self.viscosity01_edit.text(),
                viscosity1=self.viscosity02_edit.text(),
                oil0_percent=self.oil1_percent_edit.text(),
                temperature=self.temperature0_combo.currentText())
            self.mix_viscosity_label.setText('Mixture Kinematic Viscosity' +
                                             ' = ' + str(mix_viscosity) + ' ' +
                                             'cSt')
        except ValueError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except ConceptError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()

    def on_calculate_proportions_btn_clicked(self):
        try:
            proportions = OilMixture().mix_proportions(
                viscosity0=self.viscosity11_edit.text(),
                viscosity1=self.viscosity12_edit.text(),
                mix_viscosity=self.mix_viscosity_edit.text(),
                temperature=self.temperature1_combo.currentText())
            self.oil1_label.setText('1st. Oil Proportion in Mixture' + ' = ' +
                                    str(proportions[0]) + ' ' + '%')
            self.oil2_label.setText('2nd. Oil Proportion in Mixture' + ' = ' +
                                    str(proportions[1]) + ' ' + '%')
        except ValueError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except ConceptError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()


class BearingTab(BaseTab):
    """Class to implement Bearing Lubrication tab."""

    def __init__(self):
        super().__init__()
        self.text = 'Bearing Lubrication'
        self.setup_ui()
        self.grease_amount_btn.clicked.connect(
            self.on_grease_amount_button_clicked)
        self.frequency_btn.clicked.connect(self.on_frequency_button_clicked)

    def setup_ui(self):
        """Setup tab UI."""
        general_layout = QtWidgets.QVBoxLayout()
        general_layout.addWidget(self._create_grease_amount_group())
        general_layout.addWidget(self._create_frequency_group())
        self.setLayout(general_layout)

    def _create_grease_amount_group(self):
        grease_amount_gpb = QtWidgets.QGroupBox(
            'Amount of Grease for Re-lubrication')
        grease_amount_layout = QtWidgets.QFormLayout()
        self.outer_diameter_edit = QtWidgets.QLineEdit()
        self.width_edit = QtWidgets.QLineEdit()
        self.grease_amount_btn = QtWidgets.QPushButton('Calculate')
        self.grease_amount_label = QtWidgets.QLabel(
            'Amount of Grease for Re-lubrication')
        self.grease_amount_label.setFont(self.font)
        grease_amount_layout.addRow('Outer Diameter (mm):',
                                    self.outer_diameter_edit)
        grease_amount_layout.addRow('Total Width (mm):', self.width_edit)
        grease_amount_layout.addRow(self.grease_amount_btn,
                                    self.grease_amount_label)
        grease_amount_gpb.setLayout(grease_amount_layout)

        return grease_amount_gpb

    def _create_frequency_group(self):
        frequency_group = QtWidgets.QGroupBox('Re-lubrication Frequency')
        frequency_layout = QtWidgets.QFormLayout()
        frequency_group.setLayout(frequency_layout)
        self.frequency_btn = QtWidgets.QPushButton('Calculate')
        self.frequency_label = QtWidgets.QLabel('Re-lubrication Frequency')
        self.frequency_label.setFont(self.font)
        self.rpm_edit = QtWidgets.QLineEdit()
        frequency_layout.addRow('Rotation Velocity (rpm):', self.rpm_edit)
        self.inner_diameter_edit = QtWidgets.QLineEdit()
        frequency_layout.addRow('Inner Diameter (mm):',
                                self.inner_diameter_edit)
        self.ft_combo = QtWidgets.QComboBox()
        frequency_layout.addRow('Temperature:', self.ft_combo)
        self.ft_combo.addItems(('< 65°C', '65 to 80°C', '80 to 93°C',
                                '> 93°C',))
        self.fc_combo = QtWidgets.QComboBox()
        frequency_layout.addRow('Contamination:', self.fc_combo)
        self.fc_combo.addItems(('Light, no abrasive dust',
                                'Severe, no abrasive dust',
                                'Light, abrasive dust',
                                'Severe, abrasive dust'))
        self.fh_combo = QtWidgets.QComboBox()
        frequency_layout.addRow('Humidity:', self.fh_combo)
        self.fh_combo.addItems(('Relative Humidity < 80 %',
                                'Relative Humidity from 80 to 90 %',
                                'Occasional condensation',
                                'Water Presence'))
        self.fv_combo = QtWidgets.QComboBox()
        frequency_layout.addRow('Vibration:', self.fv_combo)
        self.fv_combo.addItems(('Top velocity < 0.5 cm/s',
                                'Top velocity from 0.5 to 1.0 cm/s',
                                'Top velocity > 1.0 cm/s'))
        self.fp_combo = QtWidgets.QComboBox()
        frequency_layout.addRow('Position:', self.fp_combo)
        self.fp_combo.addItems(('Horizontal', '45 Degrees', 'Vertical'))
        self.fd_combo = QtWidgets.QComboBox()
        frequency_layout.addRow('Bearing Design:', self.fd_combo)
        self.fd_combo.addItems(('Ball bearing',
                                'Cylinder/Needle roller bearing',
                                'Conical roller bearing'))
        frequency_layout.addRow(self.frequency_btn, self.frequency_label)

        return frequency_group

    def on_grease_amount_button_clicked(self):
        try:
            grease_amount = Bearing().grease_amount(
                outer_diameter=self.outer_diameter_edit.text(),
                width=self.width_edit.text())
            self.grease_amount_label.setText('Amount of Grease for '
                                             'Re-lubrication'
                                             + ' = ' + str(grease_amount)
                                             + ' ' + 'g')
        except ValueError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except ConceptError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()

    def on_frequency_button_clicked(self):
        try:
            frequency = Bearing().lubrication_frequency(
                rpm=self.rpm_edit.text(),
                inner_diameter=self.inner_diameter_edit.text(),
                ft=self.ft_combo.currentIndex(),
                fh=self.fh_combo.currentIndex(),
                fv=self.fv_combo.currentIndex(),
                fp=self.fp_combo.currentIndex(),
                fc=self.fc_combo.currentIndex(),
                fd=self.fd_combo.currentIndex())
            self.frequency_label.setText('Re-lubrication Frequency' + ' = ' +
                                         str(frequency) + ' ' + 'hours')
        except ValueError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except ConceptError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()


class AdditiveAshTab(BaseTab):
    """Class to implement Additive / Ash tab."""

    def __init__(self):
        super().__init__()
        self.text = 'Additive/Ash'
        self.setup_ui()
        self.additive_btn.clicked.connect(self.on_additive_button_clicked)
        self.total_ash_btn.clicked.connect(self.on_total_ash_button_clicked)

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

    def on_additive_button_clicked(self):
        try:
            blend = OilBlend(self.additive_percent0_edit.text())
            additive = blend.additive_percent_mass(
                additive_density=self.additive_density_edit.text(),
                oil_density=self.oil_density_edit.text())
            self.additive_label.setText('Additive' + ' = ' +
                                        str(additive) + ' ' + '% by mass')
        except ValueError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except ConceptError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()

    def on_total_ash_button_clicked(self):
        try:
            blend = OilBlend(self.additive_percent1_edit.text())

            metal_contents = {}
            for metal in OilBlend.metals():
                metal_contents[metal] = self.__dict__[metal].text()

            total_ash = blend.total_ash(**metal_contents)
            self.total_ash_label.setText('Total Ash' + ' = ' + str(total_ash) +
                                         ' % by mass')
        except ValueError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
        except ConceptError as error:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  'Error',
                                  error.__str__(),
                                  QtWidgets.QMessageBox.Ok,
                                  self).show()
