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
        pass

    @classmethod
    def metals(cls):
        return cls.contributions.keys()

    def additive_percent_mass(self, additive_density, final_oil_density):
        """Return the % by mass of Additive in a motor oil.

                             Additive Density (kg/L) * Additive (% volume)
        Additive (% mass) = ----------------------------------------------
                                Density of Finished Oil (kg/L)
        """

        return round((additive_density * self.additive_percent) /
                     final_oil_density, 2)

    def _sulfated_ash(self, metal, metal_content):
        """Return the % of sulfated ash (SA) of a motor oil.

              Metal Content (% mass) * Contribution to Ash * Additive Package (% by volume)
        SA = -------------------------------------------------------------------------------
                                                100
        """
        SA = round(metal_content * self.contributions[metal.lower()] *
                   self.additive_percent / 100, 3)

        return SA

    def total_ash(self, **metal_contents):
        total_ash = sum(self._sulfated_ash(metal, content) for
                        metal, content in metal_contents.items())
        return round(total_ash, 2)
