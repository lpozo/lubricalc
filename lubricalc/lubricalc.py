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

import math


def reynolds(V, Lc, v):
    """Return the Reynolds number (Re).

    :param
    V: velocity (m/s)

    Lc: characteristic length (m)
    For circular session Lc = D
        D: diameter
    For square session Lc = L
        L: side
    For rectangle session Lc = (2 * a * b) / (a + b)
        a, b: sides

    v: Kinematic Viscosity (m^2/s)

    :return
    Re = V * Lc / v    [(m/s m) / m^2/s]

    Re < 2000 => Laminar flow
    Re > 4000 => Turbulent flow
    """
    return round(V * Lc / v, 1)


def viscosity_index_astm_d2270(v40, v100):
    """Calculate the VI by ASTM-D2270.

    :param
    v40:  kinematic viscosity at 40°C of the oil whose viscosity
          index is to be calculated mm^2/s (cSt).
    v100: kinematic viscosity at 100°C of the oil whose viscosity
          index is to be calculated, mm^2/s (cSt)
    """
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
        if k[0] <= v100 < k[1]:
            a, b, c, d, e, f = v
            break

    # L: kinematic viscosity at 40°C of an oil of 0 viscosity
    #    index having the same kinematic viscosity at 100°C as
    #    the oil whose viscosity index is to be calculated,
    #    mm 2 /s (cSt)
    L = a * v100 ** 2 + b * v100 + c

    # H: kinematic viscosity at 40°C of an oil of 100 viscosity
    #    index having the same kinematic viscosity at 100°C as
    #    the oil whose viscosity index is to be calculated mm 2 /s
    #    (cSt)
    H = d * v100 ** 2 + e * v100 + f

    if v40 >= H:
        # Viscosity Index Up to and Including 100
        # VI = ((L - v40) / (L - H)) * 100
        return round(((L - v40) / (L - H)) * 100)

    N = (math.log10(H) - math.log10(v40)) / math.log10(v100)

    # Viscosity Index of 100 and Greater
    # VI = ((10 ** N - 1) / 0.00715) + 100
    return round(((10 ** N - 1) / 0.00715) + 100)
