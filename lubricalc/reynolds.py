#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: lubricalc.py
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

from lubricalc.validator import validate


class Reynolds:
    """Class for calculations on Reynolds Number (Re)."""

    def __init__(self):
        self._velocity = None
        self._viscosity = None
        self._length = None

    def reynolds_number(self, velocity, length, viscosity):
        """Calculate Reynolds number (Re).

              V * Lc
        Re = --------       [(m/s m) / m^2/s]
                v
        where:
        V: velocity (m/s)
        Lc: characteristic length (m)
            For circular session Lc = D
                D: diameter
            For square session Lc = L
                L: side
                                         (2 * a * b)
            For rectangular session Lc = -----------
                                           (a + b)
                a, b: sides
        v: Kinematic Viscosity (m^2/s)
        """
        # Validate input data
        self.viscosity = viscosity
        self.velocity = velocity
        self.length = length

        return round(self._velocity * self._length / self._viscosity, 1)

    def flow_type(self, velocity, length, viscosity):
        """Determine the flow type of a fluid.

        Re < 2000 => Laminar flow
        2000.0 < reynolds < 4000.0 => Mixed flow
        Re > 4000 => Turbulent flow
        """
        reynolds = self.reynolds_number(velocity, length, viscosity)
        if reynolds <= 2000.0:
            return 'laminar'
        if reynolds >= 4000.0:
            return 'turbulent'
        if 2000.0 < reynolds < 4000.0:
            return 'mixed'

    @property
    def velocity(self):
        return self._viscosity

    @velocity.setter
    def velocity(self, value):
        validate(self, 'Velocity', value, '_velocity', limit=2)

    @property
    def viscosity(self):
        return self._viscosity

    @viscosity.setter
    def viscosity(self, value):
        validate(self, 'Viscosity', value, '_viscosity', limit=2)

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        validate(self, 'Length', value, '_length', strict=True)
