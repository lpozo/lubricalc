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

from lubricalc.exception import ViscosityConceptError


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
    if v40 == 'inf' or v100 == 'inf':
        raise ValueError('Viscosity values must be valid numbers')

    try:
        v40 = float(v40)
        v100 = float(v100)
    except ValueError:
        raise ValueError('Viscosity values must be valid numbers')

    if v100 > v40:
        raise ViscosityConceptError('Viscosity at 40°C must be'
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


class Bearing:
    """Class to define calculations related with bearings."""

    def __init__(self, D, d, B, temperature, rpm):
        """Class initializer."""
        self.outer_diameter = D
        self.inner_diameter = d
        self.width = B
        self.temperature = temperature
        self.rpm = rpm

    def grease_amount(self):
        """Return the amount of grease needed for re-lubrication.

        Gg = 0.005 * D * B
        where:
        Gg: Amount of grease needed for re-lubrication (g)
        D: Outer diameter of bearing (mm)
        B: Total width of bearing (mm)
        """
        Gg = 0.005 * self.outer_diameter * self.width

        return round(Gg, 2)

    def lubrication_frequency(self, contamination, moisture,
                              vibration, position, design):
        """Return the re-lubrication frequency.
                    14000000
        T = K * [(--------------) - 4 * d]
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
                Top speed < 0.2 ips (inch per second) then Fv = 1.0
                0.2 to 0.4 ips, then Fv = 0.6
                > 0.4 ips, then Fv = 0.3
            Fp: Shaft position factor
                Horizontal, then Fp = 1.0
                45 degrees, then Fp = 0.5
                Vertical, then Fp = 0.3
            Fd: Bearing design factor
                Ball bearing, then Fd = 10
                Cylinder/Needle roller bearing, then Fd = 5
                Conical roller bearing, then Fd = 1
        n: Rotation speed (rpm)
        d: Inner diameter of the bearing (mm)
        """
        Ft = self._claculate_Ft()

        Fc = self._calculate_Fc(contamination)

        Fh = self._calculate_Fh(moisture)

        Fv = self._calculate_Fv(vibration)

        Fp = self._calculate_Fp(position)

        Fd = self._calculate_Fd(design)

        K = Ft * Fc * Fh * Fv * Fp * Fd

        T = K * ((14_000_000 / (self.rpm * math.sqrt(self.inner_diameter))) -
                 4 * self.inner_diameter)

        return round(T)

    def speed_factor(self):
        """Return the speed factor of a bearing.

        A = n * dm
        where:
        A: Speed factor (mm/min)
        n: rotation speed (rpm)
        dm: mean diameter (mm)
             (D + d)
        dm = -------
                2
        """
        return self.rpm * (self.outer_diameter + self.inner_diameter) / 2

    def _claculate_Ft(self):
        up = float('inf')
        ft_map = {(0, 65.0): 1.0,
                  (65.0, 80.0): 0.5,
                  (80.0, 93.0): 0.2,
                  (93.0, up): 0.1}

        Ft = None
        for k, v in ft_map.items():
            if k[0] <= self.temperature < k[1]:
                Ft = v
                break

        return Ft

    def _calculate_Fc(self, item):
        fc_map = (1.0, 0.7, 0.4, 0.2)
        return fc_map[item]

    def _calculate_Fh(self, item):
        fh_map = (1.0, 0.7, 0.4, 0.1)
        return fh_map[item]

    def _calculate_Fv(self, item):
        fv_map = (1.0, 0.6, 0.3)
        return fv_map[item]

    def _calculate_Fp(self, item):
        fp_map = (1.0, 0.5, 0.3)
        return fp_map[item]

    def _calculate_Fd(self, item):
        fd_map = (10.0, 5.0, 1.0)
        return fd_map[item]


class OilBlend:
    """Class to calculate some parameters of a motor oil blend."""
    def __init__(self, additive_percent=0.0):
        self.additive_percent = additive_percent
        self.contributions = {'zinc': 1.50,
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

    @property
    def metals(self):
        return self.contributions.keys()

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


def oil_mix(KV1, KV2, oil1_percent, temperature):
    """Return the resulting viscosity of a mix of different bases."""
    KV1 = float(KV1)
    KV2 = float(KV2)
    temp_map = {'100': 1.8,
                '40': 4.1,
                '-5': 1.9}
    K = temp_map[temperature]
    x1 = float(oil1_percent) / 100
    mix_KV = (math.exp(math.log(KV2 + K) *
                       math.exp(x1 * math.log(
                           math.log(KV1 + K) /
                           math.log(KV2 + K)))) - K)
    return round(mix_KV, 2)
