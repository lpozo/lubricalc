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

from nose import run
from lubricalc.lubricalc import *


class TestLubricalc:
    """Class to test Lubricalc."""

    def test_reynolds(self):
        assert reynolds(15, 0.01, 0.00015) == 1000

    def test_viscosity_index_astm_d2270_156(self):
        assert viscosity_index_astm_d2270(v40=22.83, v100=5.05) == 156

    def test_viscosity_index_astm_d2270_92(self):
        assert viscosity_index_astm_d2270(v40=73.3, v100=8.86) == 92

    def test_viscosity_index_astm_d2270_146(self):
        assert viscosity_index_astm_d2270(v40=138.9, v100=18.1) == 145

class TestSulfatedAsh:
    """Class to test SulfatedAsh."""

    def test_additive_percent_mass(self):
        obj = SulfatedAsh(8.0)
        assert obj.additive_percent_mass(additive_density=0.959,
                                         final_oil_density=0.881) == 8.71

    def test_total_ash(self):
        obj = SulfatedAsh(additive_percent=8.5)
        assert obj.total_ash(Calcium=0.47,
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



if __name__ == '__main__':
    run()
