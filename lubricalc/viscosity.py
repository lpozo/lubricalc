# -*- coding: utf-8 -*-

# File name: viscosity.py
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

"""This module provides Viscosity Class."""

import math

from .exception import InvertedViscosityError
from .exception import ConceptError
from .validator import validate


class Viscosity:
    """Class for calculations on Viscosity."""

    def __init__(self):
        self._viscosity40 = None
        self._viscosity100 = None
        self._v_index = None

    def viscosity_index(self, viscosity40, viscosity100):
        """Calculate the Viscosity Index (VI) by ASTM-D2270.

        - Viscosity Index Up to and Including 100

               (L - KV40)
        VI = ------------- * 100
                (L - H)

        where:

        KV40:  kinematic viscosity at 40°C of the oil whose viscosity
               index is to be calculated mm^2/s (cSt).
        KV100: kinematic viscosity at 100°C of the oil whose viscosity
               index is to be calculated, mm^2/s (cSt)
        L: kinematic viscosity at 40°C of an oil of 0 viscosity
           index having the same kinematic viscosity at 100°C as
           the oil whose viscosity index is to be calculated,
           mm^2/s (cSt)
           L = a * KV100 ** 2 + b * KV100 + c
           a, b, c: interpolation coefficients
        H: kinematic viscosity at 40°C of an oil of 100 viscosity
           index having the same kinematic viscosity at 100°C as
           the oil whose viscosity index is to be calculated mm 2 /s
           (cSt)
           H = d * KV100 ** 2 + e * KV100 + f
           d, e, f: interpolation coefficients

        - Viscosity Index of 100 and Greater

                (10^N - 1)
        VI = --------------- + 100
                 0.00715

        where:

              log10(H) - log10(KV40)
        N = --------------------------
                   log10(KV100)
        """
        # Validate Data
        self.viscosity40 = viscosity40
        self.viscosity100 = viscosity100
        if self._viscosity100 > self._viscosity40:
            raise InvertedViscosityError('Viscosity at 40°C must be'
                                         ' greater than Viscosity at 100°C')

        up = float('inf')
        coefficients = {
             (2, 3.8): (1.14673, 1.7576, -0.109, 0.84155, 1.5521, -0.077),
             (3.8, 4.4): (3.38095, -15.4952, 33.196, 0.78571, 1.7929, -0.183),
             (4.4, 5): (2.5, -7.2143, 13.812, 0.82143, 1.5679, 0.119),
             (5, 6.4): (0.101, 16.635, -45.469, 0.04985, 9.1613, -18.557),
             (6.4, 7): (3.35714, -23.5643, 78.466, 0.22619, 7.7369, -16.656),
             (7, 7.7): (0.01191, 21.475, -72.870, 0.79762, -0.7321, 14.61),
             (7.7, 9): (0.41858, 16.1558, -56.040, 0.05794, 10.5156, -28.240),
             (9, 12): (0.88779, 7.5527, -16.600, 0.26665, 6.7015, -10.810),
             (12, 15): (0.7672, 10.7972, -38.180, 0.20073, 8.4658, -22.490),
             (15, 18): (0.97305, 5.3135, -2.200, 0.28889, 5.9741, -4.930),
             (18, 22): (0.97256, 5.25, -0.980, 0.24504, 7.416, -16.730),
             (22, 28): (0.91413, 7.4759, -21.820, 0.20323, 9.1267, -34.230),
             (28, 40): (0.87031, 9.7157, -50.770, 0.18411, 10.1015, -46.750),
             (40, 55): (0.84703, 12.6752, -133.310, 0.17029, 11.4866, -80.620),
             (55, 70): (0.85921, 11.1009, -83.19, 0.1713, 11.368, -76.940),
             (70, up): (0.83531, 14.6731, -216.246, 0.16841, 11.8493, -96.947)
        }

        a, b, c, d, e, f = [0] * 6

        for k, v in coefficients.items():
            if k[0] <= self._viscosity100 < k[1]:
                a, b, c, d, e, f = v
                break

        L = a * self._viscosity100 ** 2 + b * self._viscosity100 + c

        H = d * self._viscosity100 ** 2 + e * self._viscosity100 + f

        if self._viscosity40 >= H:
            v_index = round(((L - self._viscosity40) / (L - H)) * 100)
            self._validate_viscosity_index(v_index)
            return v_index

        N = ((math.log10(H) - math.log10(self._viscosity40)) /
             math.log10(self._viscosity100))
        v_index = round(((10 ** N - 1) / 0.00715) + 100)
        self._validate_viscosity_index(v_index)
        return v_index

    def _validate_viscosity_index(self, v_index):
        if v_index < 0 or v_index > 300:
            raise ConceptError('Viscosity Index: not defined')

    def viscosity_at_40(self, viscosity100, v_index):
        """Calculate the Kinematic Viscosity at 40°C."""
        # Validate Data
        self.viscosity100 = viscosity100
        self.v_index = v_index
        self._validate_viscosity_index(self._v_index)

        temp_v_index = self._v_index
        n = self._viscosity100
        while temp_v_index >= self._v_index and n <= 2000:
            temp_v_index = self.viscosity_index(n, self._viscosity100)
            n += 0.05
        return round((n * 100 + 0.1) / 100, 2)

    def viscosity_at_100(self, viscosity40, v_index):
        """Calculate the Kinematic Viscosity at 100°C."""
        # Validate Data
        self.viscosity40 = viscosity40
        self.v_index = v_index
        self._validate_viscosity_index(self._v_index)

        temp_v_index = self._v_index
        n = 2.0
        while temp_v_index <= self._v_index and n <= 500.0:
            temp_v_index = self.viscosity_index(self._viscosity40, n)
            n += 0.01
        return round((n * 100 + 0.01) / 100, 2)

    @property
    def viscosity40(self):
        return self._viscosity40

    @viscosity40.setter
    def viscosity40(self, value):
        validate(self, 'Viscosity at 40°C', value, '_viscosity40', limit=1.99)

    @property
    def viscosity100(self):
        return self._viscosity100

    @viscosity100.setter
    def viscosity100(self, value):
        validate(self, 'Viscosity at 100°C', value, '_viscosity100', limit=1.99)

    @property
    def v_index(self):
        return self._v_index

    @v_index.setter
    def v_index(self, value):
        validate(self, 'Viscosity Index', value, '_v_index')
