# -*- coding: utf-8 -*-

# File name: blend.py
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

"""This module provides OilBlend Class."""

from lubricalc.validator import validate


class OilBlend:
    """Class to calculate some parameters of a motor oil blend."""

    contributions = {'zinc': 1.50,
                     'barium': 1.70,
                     'sodium': 3.09,
                     'calcium': 3.40,
                     'magnesium': 4.95,
                     'lead': 1.464,
                     'boron': 3.22,
                     'potassium': 2.23,
                     'manganese': 1.291,
                     'molybdenum': 1.5,
                     'copper': 1.252}

    def __init__(self, additive_percent):
        self._additive_percent = None
        self.additive_percent = additive_percent
        self._additive_density = None
        self._oil_density = None
        self._metal_content = None

    @classmethod
    def metals(cls):
        return cls.contributions.keys()

    def additive_percent_mass(self, additive_density, oil_density):
        """Calculate the % by mass of Additive in a motor oil.

                                Additive Density (kg/L) * Additive (% volume)
        Additive (% mass) = ---------------------------------------------------
                                       Density of Finished Oil (kg/L)
        """
        # Data Validation
        self.additive_density = additive_density
        self.oil_density = oil_density

        return round((self._additive_density * self._additive_percent) /
                     self._oil_density, 2)

    def _sulfated_ash(self, metal, metal_content):
        """Calculate the % of sulfated ash (SA) of a motor oil.

              Metal Content (% mass) * Contribution to Ash * Additive Package (% by volume)
        SA = -------------------------------------------------------------------------------
                                                100
        """
        # Data Validation
        self.metal_content = metal_content

        ash = (self._metal_content * self.contributions[metal.lower()] *
               self._additive_percent / 100)

        return round(ash, 3)

    def total_ash(self, **metal_contents):
        total_ash = sum(self._sulfated_ash(metal, content) for
                        metal, content in metal_contents.items())
        return round(total_ash, 2)

    @property
    def additive_percent(self):
        return self._additive_percent

    @additive_percent.setter
    def additive_percent(self, value):
        validate(self, 'Additive (% volume)', value, '_additive_percent',
                 strict=True)

    @property
    def additive_density(self):
        return self._additive_density

    @additive_density.setter
    def additive_density(self, value):
        validate(self, 'Additive Density', value, '_additive_density',
                 strict=True)

    @property
    def oil_density(self):
        return self._oil_density

    @oil_density.setter
    def oil_density(self, value):
        validate(self, 'Finished Oil Density', value, '_oil_density',
                 strict=True)

    @property
    def metal_content(self):
        return self._metal_content

    @metal_content.setter
    def metal_content(self, value):
        if value == '':
            self._metal_content = 0.0
        else:
            validate(self, 'Metal Content', value, '_metal_content')
