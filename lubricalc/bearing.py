# -*- coding: utf-8 -*-

# File name: bearing.py
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

"""This module provides Bearing Class."""

import math

from .validator import Validator


class Bearing:
    """Class to define calculations related with bearings."""

    def __init__(self):
        self._outer_diameter = None
        self._inner_diameter = None
        self._width = None
        self._rpm = None
        self._validator = Validator()

    def grease_amount(self, outer_diameter, width):
        """Return the amount of grease needed for re-lubrication.

        Gg = 0.005 * D * B
        where:
        Gg: Amount of grease needed for re-lubrication (g)
        D: Outer diameter of bearing (mm)
        B: Total width of bearing (mm)
        """

        # Validate Data
        self.outer_diameter = outer_diameter
        self.width = width

        grease_amount = 0.005 * self._outer_diameter * self._width

        return round(grease_amount, 2)

    def lubrication_frequency(self, rpm, inner_diameter, **factors):
        """Calculate the re-lubrication frequency in hours.

                       14000000
        T = K * [(------------------) - 4 * d]
                      n * sqrt(d)

        where:
        T: Frequency of re-lubrication (hours)
        K: Corrections factors
            K = Ft * Fc * Fh * Fv * Fp * Fd
            where:
            Ft: Temperature of bearing housing factor
                < 65°C, then Ft = 1.0
                65 to 80°C, then Ft = 0.5
                80 to 93°C, then Ft = 0.2
                > 93°C, then Ft = 0.1
            Fc: Solid contamination factor
                Light, no abrasive dust, then Fc = 1.0
                Severe, no abrasive dust, then Fc = 0.7
                Light, abrasive dust, then Fc = 0.4
                Severe, abrasive dust, then Fc = 0.2
            Fh: Moisture factor
                < 80 % ,then Fh = 1.0
                80 to 90 %, then Fh = 0.7
                Occasional condensation, then Fh = 0.4
                Water, then Fh = 0.2
            Fv: Vibrations factor
                Top velocity < 0.5 cm/s, then Fv = 1.0
                0.5 to 1.0 cm/s, then Fv = 0.6
                > 1.0 cm/s, then Fv = 0.3
            Fp: Shaft position factor
                Horizontal, then Fp = 1.0
                45 degrees, then Fp = 0.5
                Vertical, then Fp = 0.3
            Fd: Bearing design factor
                Ball bearing, then Fd = 10
                Cylinder/Needle roller bearing, then Fd = 5
                Conical roller bearing, then Fd = 1
        n: Rotation velocity (rpm)
        d: Inner diameter of the bearing (mm)
        """
        # Validate Data
        self.inner_diameter = inner_diameter
        self.rpm = rpm

        factors_map = {'ft': (1.0, 0.5, 0.2, 0.1),
                       'fc': (1.0, 0.7, 0.4, 0.2),
                       'fh': (1.0, 0.7, 0.4, 0.1),
                       'fv': (1.0, 0.6, 0.3),
                       'fp': (1.0, 0.5, 0.3),
                       'fd': (10.0, 5.0, 1.0)}

        k_factor = 1

        for k, v in factors.items():
            v = int(v)
            k_factor *= factors_map[k][v]

        frequency = k_factor * ((14_000_000 / (self._rpm * math.sqrt(
            self._inner_diameter))) - 4 * self._inner_diameter)

        return round(frequency)

    def velocity_factor(self, outer_diameter, inner_diameter, rpm):
        """Calculate the velocity factor of a bearing.

        A = n * dm
        where:
        A: Velocity factor (mm/min)
        n: Rotation velocity (rpm)
        dm: Mean diameter (mm)
               (D + d)
        dm = -----------
                  2
        """
        # Validate Data
        self.outer_diameter = outer_diameter
        self.inner_diameter = inner_diameter
        self.rpm = rpm

        factor = self._rpm * (self._outer_diameter + self._inner_diameter) / 2

        return round(factor)

    @property
    def outer_diameter(self):
        return self._outer_diameter

    @outer_diameter.setter
    def outer_diameter(self, value):
        self._setter('Outer Diameter', value, '_outer_diameter')

    @property
    def inner_diameter(self):
        return self._inner_diameter

    @inner_diameter.setter
    def inner_diameter(self, value):
        self._setter('Inner Diameter', value, '_inner_diameter')

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._setter('Width', value, '_width')

    @property
    def rpm(self):
        return self._rpm

    @rpm.setter
    def rpm(self, value):
        self._setter('Velocity', value, '_rpm')

    def _setter(self, name, value, attr, limit=0):
        value = self._validator.validate_float(name, value)
        lower_limit = limit
        self._validator.validate_lower_limit(name, value, lower_limit)
        setattr(self, attr, value)
