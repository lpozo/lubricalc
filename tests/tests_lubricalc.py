#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: tests.py
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

"""This module provides tests for cli.py."""

import nose

from lubricalc.lubricalc import *


class TestReynolds:
    """Class to test Reynolds."""

    def test_reynolds_float_input(self):
        assert reynolds(15.0, 0.01, 0.00015) == 1000

    def test_reynolds_int_input(self):
        assert reynolds(15, 10, 15) == 10

    def test_reynolds_strings_input(self):
        assert reynolds('15', '0.01', '0.00015') == 1000

    def test_reynolds_stings_coma_input(self):
        assert reynolds('15,0', '0,01', '0,00015') == 1000

    @nose.tools.raises(ConceptError)
    def test_reynolds_negative_input(self):
        reynolds('-15,0', '0,01', '0,00015')

    @nose.tools.raises(ConceptError)
    def test_reynolds_viscosity_zero_input(self):
        reynolds('15,0', '0,05', '0,0')

    @nose.tools.raises(ConceptError)
    def test_reynolds_zero_input(self):
        reynolds('0', '0,05', '0,00015')

    @nose.tools.raises(InfiniteValueError)
    def test_reynolds_inf_input(self):
        reynolds(float('inf'), 0.01, 0.00015)


class TestViscosityIndex:
    """Class to test viscosity_index."""

    def test_viscosity_index_156(self):
        assert viscosity_index(KV40=22.83, KV100=5.05) == 156

    def test_viscosity_index_92(self):
        assert viscosity_index(KV40=73.3, KV100=8.86) == 92

    def test_viscosity_index_145(self):
        assert viscosity_index(KV40=138.9, KV100=18.1) == 145

    def test_viscosity_index_string_input(self):
        assert viscosity_index(KV40='138.9', KV100='18.1') == 145

    def test_viscosity_index_coma_input(self):
        assert viscosity_index(KV40='138,9', KV100='18,1') == 145

    @nose.tools.raises(InfiniteValueError)
    def test_viscosity_index_inf_input(self):
        viscosity_index(KV40=float('inf'), KV100='18,1')

    @nose.tools.raises(ConceptError)
    def test_viscosity_index_cero_kv40_input(self):
        viscosity_index(KV40=0, KV100='18,1')

    @nose.tools.raises(ConceptError)
    def test_viscosity_index_cero_kv100_input(self):
        viscosity_index(KV40=150, KV100=0)

    @nose.tools.raises(ConceptError)
    def test_viscosity_index_cero_kv40_lt_kv100_input(self):
        viscosity_index(KV40=15, KV100=150)

class TestOilMixture:
    """Class to test OilMixture class"""

    def test_oil_mix(self):
        mix = OilMixture()
        assert mix.oil_mix(20, 16, 45, '100') == 17.67

    def test_mix_proportions(self):
        mix = OilMixture()
        assert mix.mix_proportions(460, 150, 680, '40') == (23.64, 76.36)


class TestOilBlend:
    """Class to test OilBlend."""

    def test_additive_percent_mass(self):
        blend = OilBlend(8.0)
        assert blend.additive_percent_mass(additive_density=0.959,
                                           final_oil_density=0.881) == 8.71

    def test_total_ash(self):
        blend = OilBlend(additive_percent=8.5)
        assert blend.total_ash(Calcium=0.47,
                               Magnesium=1.15,
                               zinc=1.66) == 0.83


class TestBearing:
    """Class to test Bearing class."""

    def test_grease_amount(self):
        """Test grease_amount()."""
        bearing = Bearing(25, 18, 60, 12, 1750)
        assert bearing.grease_amount() == 7.5

    def test_lubrication_frequency(self):
        """Test lubrication_frequency()."""
        bearing = Bearing(25, 18, 60, 12, 1750)
        assert bearing.lubrication_frequency(contamination=1,
                                             moisture=2,
                                             vibration=0,
                                             position=0,
                                             design=2) == 508

    def test_speed_factor(self):
        """Test speed_factor()."""
        bearing = Bearing(58, 45, 12, 60, 3000)
        assert bearing.speed_factor() == 154500


if __name__ == '__main__':
    nose.run()
