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

from lubricalc.exception import *


def reynolds_number(velocity, length, viscosity):
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
    velocity, length, viscosity = _validate_float(velocity, length, viscosity)
    _validate_concepts(velocity, length, viscosity)

    return round(velocity * length / viscosity, 1)


def flow_type(velocity, length, viscosity):
    """Determine the flow type of a fluid.

    Re < 2000 => Laminar flow
    2000.0 < reynolds < 4000.0 => Mixed flow
    Re > 4000 => Turbulent flow
    """
    reynolds = reynolds_number(velocity, length, viscosity)
    if reynolds <= 2000.0:
        return 'laminar'
    if reynolds >= 4000.0:
        return 'turbulent'
    if 2000.0 < reynolds < 4000.0:
        return 'mixed'


def _validate_float(*data):
    """Validate the input data."""
    validated_data = []
    for datum in data:
        datum = str(datum).replace(',', '.').strip()
        try:
            datum = float(datum)
            validated_data.append(datum)
        except ValueError:
            raise ValueError('Input value must be a valid number')

        if datum == float('inf'):
            raise InfiniteValueError('Input value must not be infinite')

    if validated_data.__len__() == 1:
        return validated_data[0]
    return validated_data


def _validate_concepts(*data):
    """Validate the concept of input data."""
    for datum in data:
        if datum <= 0:
            raise ConceptError('Input value is a concept error')


def _validate_viscosity(*data):
    for datum in data:
        if datum < 2:
            raise ConceptError('Input value is a concept error')


def viscosity_index(viscosity_40, viscosity_100):
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
    viscosity_40, viscosity_100 = _validate_float(viscosity_40, viscosity_100)
    if viscosity_100 > viscosity_40:
        raise InvertedViscosityError('Viscosity at 40°C must be'
                                     ' greater than Viscosity at 100°C')
    _validate_viscosity(viscosity_40, viscosity_100)

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
        if k[0] <= viscosity_100 < k[1]:
            a, b, c, d, e, f = v
            break

    L = a * viscosity_100 ** 2 + b * viscosity_100 + c

    H = d * viscosity_100 ** 2 + e * viscosity_100 + f

    if viscosity_40 >= H:
        return round(((L - viscosity_40) / (L - H)) * 100)

    N = (math.log10(H) - math.log10(viscosity_40)) / math.log10(viscosity_100)

    return round(((10 ** N - 1) / 0.00715) + 100)


def viscosity_at_40(viscosity_100, v_index):
    """Calculate the Kinematic Viscosity at 40°C."""
    viscosity_100, v_index = _validate_float(viscosity_100, v_index)
    _validate_viscosity(viscosity_100)

    temp_v_index = v_index
    n = viscosity_100
    while temp_v_index >= v_index and n <= 2000:
        temp_v_index = viscosity_index(n, viscosity_100)
        n += 0.05
    return round((n * 100 + 0.1) / 100, 2)


def viscosity_at_100(viscosity_40, v_index):
    """Calculate the Kinematic Viscosity at 100°C."""
    viscosity_40, v_index = _validate_float(viscosity_40, v_index)
    _validate_viscosity(viscosity_40)

    temp_v_index = v_index
    n = 2
    while temp_v_index <= v_index and n <= 500.0:
        temp_v_index = viscosity_index(viscosity_40, n)
        n += 0.01
    return round((n * 100 + 0.01) / 100, 2)


class Bearing:
    """Class to define calculations related with bearings."""

    @classmethod
    def grease_amount(cls, outer_diameter, width):
        """Return the amount of grease needed for re-lubrication.

        Gg = 0.005 * D * B
        where:
        Gg: Amount of grease needed for re-lubrication (g)
        D: Outer diameter of bearing (mm)
        B: Total width of bearing (mm)
        """

        outer_diameter, width = _validate_float(outer_diameter, width)
        _validate_concepts(outer_diameter, width)

        grease_amount = 0.005 * outer_diameter * width

        return round(grease_amount, 2)

    @classmethod
    def lubrication_frequency(cls, rpm, inner_diameter, **factors):
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
                Top speed < 0.5 cm/s, then Fv = 1.0
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
        n: Rotation speed (rpm)
        d: Inner diameter of the bearing (mm)
        """
        factors_map = {'ft': (1.0, 0.5, 0.2, 0.1),
                       'fc': (1.0, 0.7, 0.4, 0.2),
                       'fh': (1.0, 0.7, 0.4, 0.1),
                       'fv': (1.0, 0.6, 0.3),
                       'fp': (1.0, 0.5, 0.3),
                       'fd': (10.0, 5.0, 1.0)}

        rpm, inner_diameter = _validate_float(rpm, inner_diameter)
        _validate_concepts(rpm, inner_diameter)

        k_factor = 1

        for k, v in factors.items():
            v = int(v)
            k_factor *= factors_map[k][v]

        frequency = k_factor * ((14_000_000 /
                                 (rpm * math.sqrt(inner_diameter))) -
                                4 * inner_diameter)

        return round(frequency)

    @classmethod
    def speed_factor(cls, outer_diameter, inner_diameter, rpm):
        """Calculate the speed factor of a bearing.

        A = n * dm
        where:
        A: Speed factor (mm/min)
        n: rotation speed (rpm)
        dm: mean diameter (mm)
               (D + d)
        dm = -----------
                  2
        """
        return rpm * (outer_diameter + inner_diameter) / 2


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
        self.additive_percent = _validate_float(additive_percent)
        _validate_concepts(self.additive_percent)

    @classmethod
    def metals(cls):
        return cls.contributions.keys()

    def additive_percent_mass(self, additive_density, final_oil_density):
        """Return the % by mass of Additive in a motor oil.

                             Additive Density (kg/L) * Additive (% volume)
        Additive (% mass) = ----------------------------------------------
                                Density of Finished Oil (kg/L)
        """
        additive_density, final_oil_density = _validate_float(
            additive_density, final_oil_density)
        _validate_concepts(additive_density, final_oil_density)

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


class OilMixture:

    def __init__(self):
        self.temp_map = {'100': 1.8,
                         '40': 4.1,
                         '-5': 1.9}

    def oil_mix(self, KV1, KV2, oil1_percent, temperature):
        """Return the resulting viscosity of a mix of different bases."""
        KV1 = float(KV1)
        KV2 = float(KV2)
        K = self.temp_map[temperature]
        x1 = float(oil1_percent) / 100
        mix_KV = (math.exp(math.log(KV2 + K) *
                           math.exp(x1 * math.log(
                               math.log(KV1 + K) /
                               math.log(KV2 + K)))) - K)

        return round(mix_KV, 2)

    def mix_proportions(self, KV, KV1, KV2, temperature):
        """Return proportions to get a mixture of a given viscosity."""
        KV = float(KV)
        KV1 = float(KV1)
        KV2 = float(KV2)
        K = self.temp_map[temperature]
        a = math.log(KV + K)
        b = math.log(KV1 + K)
        c = math.log(KV2 + K)
        oil1_percent = 10000 * (math.log(a / c) / math.log(b / c)) / 100
        oil2_percent = 100 - oil1_percent

        return round(oil1_percent, 2), round(oil2_percent, 2)
