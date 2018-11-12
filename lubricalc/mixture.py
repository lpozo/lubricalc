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
