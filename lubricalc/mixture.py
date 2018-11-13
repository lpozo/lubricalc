# -*- coding: utf-8 -*-

# File name: mixture.py
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

"""This module provides OilMixture Class."""

import math

from .exception import NotInIntervalViscosityError
from .validator import Validator


class OilMixture:
    """Class to provide calculations on motor oil mixtures."""

    def __init__(self):
        self._viscosity0 = None
        self._viscosity1 = None
        self._mix_viscosity = None
        self._oil0_percent = None
        self._validator = Validator()
        self.temp_map = {'100': 1.8,
                         '40': 4.1,
                         '-5': 1.9}

    def oil_mix_viscosity(self, viscosity0, viscosity1,
                          oil0_percent, temperature):
        """Return the resulting viscosity of a mix of different bases."""
        # Validate Data
        self.viscosity0 = viscosity0
        self.viscosity1 = viscosity1
        self.oil0_percent = oil0_percent

        K = self.temp_map[temperature]
        x1 = self._oil0_percent / 100
        a = math.log(self._viscosity1 + K)
        b = math.log(self._viscosity0 + K)
        mix_viscosity = (math.exp(a * math.exp(x1 * math.log(b / a))) - K)

        return round(mix_viscosity, 2)

    def mix_proportions(self, viscosity0, viscosity1,
                        mix_viscosity, temperature):
        """Return proportions to get a mixture of a given viscosity."""
        # Validate Data
        self.viscosity0 = viscosity0
        self.viscosity1 = viscosity1
        self.mix_viscosity = mix_viscosity

        if not(self._viscosity0 < self._mix_viscosity < self._viscosity1 or
                self._viscosity1 < self._mix_viscosity < self._viscosity0):
            raise NotInIntervalViscosityError('Mixture viscosity must be in '
                                              'between viscosity interval')

        K = self.temp_map[temperature]
        a = math.log(self.mix_viscosity + K)
        b = math.log(self._viscosity0 + K)
        c = math.log(self._viscosity1 + K)
        oil1_percent = 10000 * (math.log(a / c) / math.log(b / c)) / 100
        oil2_percent = 100 - oil1_percent

        return round(oil1_percent, 2), round(oil2_percent, 2)

    @property
    def viscosity0(self):
        return self._viscosity0

    @viscosity0.setter
    def viscosity0(self, value):
        self._setter('Fist Oil Viscosity', value, '_viscosity0', limit=1.99)

    @property
    def viscosity1(self):
        return self._viscosity1

    @viscosity1.setter
    def viscosity1(self, value):
        self._setter('Second Oil Viscosity', value, '_viscosity1', limit=1.99)

    @property
    def mix_viscosity(self):
        return self._mix_viscosity

    @mix_viscosity.setter
    def mix_viscosity(self, value):
        self._setter('Mixture Viscosity', value, '_mix_viscosity', limit=1.99)

    @property
    def oil0_percent(self):
        return self._mix_viscosity

    @oil0_percent.setter
    def oil0_percent(self, value):
        self._setter('First Oil Percent in Mix', value, '_oil0_percent',
                     limit=1.99)

    def _setter(self, name, value, attr, limit=0.0):
        value = self._validator.validate_float(name, value)
        lower_limit = limit
        self._validator.validate_lower_limit(name, value, lower_limit)
        setattr(self, attr, value)
