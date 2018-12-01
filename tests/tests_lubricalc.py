#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: tests_libricalc.py
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

"""This module provides tests for lubricalc package."""

import nose

from lubricalc.exception import ConceptError
from lubricalc.exception import InvertedViscosityError
from lubricalc.exception import ViscosityIntervalError
from lubricalc.bearing import Bearing
from lubricalc.blend import OilBlend
from lubricalc.mixture import OilMixture
from lubricalc.reynolds import Reynolds
from lubricalc.validator import Validator
from lubricalc.viscosity import Viscosity


class TestValidator:
    """Class to test Validator class."""
    validator = Validator()

    def test_validate_float(self):
        assert self.validator.validate_float('Variable', 1.02) == 1.02

    def test_validate_float_string_float_input(self):
        assert self.validator.validate_float('Variable', '1.02') == 1.02

    def test_validate_float_string_spaced_input(self):
        assert self.validator.validate_float('Variable', ' 1.02   ') == 1.02

    def test_validate_float_string_coma_input(self):
        assert self.validator.validate_float('Variable', '1,02') == 1.02

    @nose.tools.raises(ValueError)
    def test_validate_float_inf_input(self):
        self.validator.validate_float('Variable', 'inf')

    @nose.tools.raises(ValueError)
    def test_validate_float_negative_inf_input(self):
        self.validator.validate_float('Variable', '-inf')

    @nose.tools.raises(ValueError)
    def test_validate_float_empty_string_input(self):
        self.validator.validate_float('Variable', '')

    @nose.tools.raises(ValueError)
    def test_validate_float_string_input(self):
        self.validator.validate_float('Variable', 'string')

    def test_validate_float_int_input(self):
        assert self.validator.validate_float('Variable', 10) == 10.0

    @nose.tools.raises(ConceptError)
    def test_validate_lower_limit(self):
        self.validator.validate_lower_limit('Variable', 15, 16)

    def test_validate_lower_limit_none(self):
        assert self.validator.validate_lower_limit(15, 14) is None


class TestReynolds:
    """Class to test Reynolds."""

    def test_reynolds_float_input(self):
        assert Reynolds().reynolds_number(15.0, 0.10, 3) == 0.5

    def test_reynolds_int_input(self):
        assert Reynolds().reynolds_number(15, 10, 15) == 10

    def test_reynolds_strings_input(self):
        assert Reynolds().reynolds_number('15', '0.10', '3') == 0.5

    def test_reynolds_strings_space_input(self):
        assert Reynolds().reynolds_number('15 ', '  0.10', ' 3  ') == 0.5

    def test_reynolds_stings_coma_input(self):
        assert Reynolds().reynolds_number('15,0', '0,10', '3,0') == 0.5

    @nose.tools.raises(ConceptError)
    def test_reynolds_negative_input(self):
        Reynolds().reynolds_number('-15,0', '0,01', '2')

    @nose.tools.raises(ConceptError)
    def test_reynolds_viscosity_zero_input(self):
        Reynolds().reynolds_number('15,0', '0,05', '0,0')

    @nose.tools.raises(ConceptError)
    def test_reynolds_zero_input(self):
        Reynolds().reynolds_number('0', '0,05', '2')

    @nose.tools.raises(ValueError)
    def test_reynolds_inf_input(self):
        Reynolds().reynolds_number(float('inf'), 0.01, 3.0)


class TestViscosity:
    """Class to test Viscosity class."""

    def test_viscosity_index_156(self):
        assert Viscosity().viscosity_index(22.83, 5.05) == 156

    def test_viscosity_index_92(self):
        assert Viscosity().viscosity_index(73.3, 8.86) == 92

    def test_viscosity_index_145(self):
        assert Viscosity().viscosity_index(138.9, 18.1) == 145

    def test_viscosity_index_string_input(self):
        assert Viscosity().viscosity_index('138.9', '18.1') == 145

    def test_viscosity_index_coma_input(self):
        assert Viscosity().viscosity_index('138,9', '18,1') == 145

    @nose.tools.raises(ValueError)
    def test_viscosity_index_inf_input(self):
        Viscosity().viscosity_index(float('inf'), '18,1')

    @nose.tools.raises(ConceptError)
    def test_viscosity_index_cero_kv40_input(self):
        Viscosity().viscosity_index(0, '18,1')

    @nose.tools.raises(ConceptError)
    def test_viscosity_index_cero_kv100_input(self):
        Viscosity().viscosity_index(150, 0)

    @nose.tools.raises(InvertedViscosityError)
    def test_viscosity_index_kv40_lt_kv100_input(self):
        Viscosity().viscosity_index(15, 150)

    @nose.tools.raises(ConceptError)
    def test_viscosity_index_input_lt_2(self):
        Viscosity().viscosity_index(1.5, 1)

    def test_viscosity_at_40(self):
        assert Viscosity().viscosity_at_40(15, v_index=130) == 119.6

    def test_viscosity_at_100(self):
        assert Viscosity().viscosity_at_100(112, v_index=140) == 15.12

    def test_viscosity_at_20_iso5(self):
        assert Viscosity().viscosity_at_any_temp(4.6, 2, 20) == 6.89

    def test_viscosity_at_20_iso46(self):
        assert Viscosity().viscosity_at_any_temp(46, 7, 20) == 130.66

    def test_viscosity_at_35_iso46(self):
        assert Viscosity().viscosity_at_any_temp(46, 7, 35.0) == 58.08

    def test_viscosity_at_35_iso46_string_input(self):
        assert Viscosity().viscosity_at_any_temp('46', '7 ', '35.0') == 58.08

    @nose.tools.raises(ConceptError)
    def test_viscosity_lt_273_iso46(self):
        Viscosity().viscosity_at_any_temp('46', '7 ', '-275')


class TestOilMixture:
    """Class to test OilMixture class."""

    def test_oil_mix_viscosity(self):
        assert OilMixture().oil_mix_viscosity(20, 16, 45, '100') == 17.67

    def test_oil_mix_viscosity_string_input(self):
        assert OilMixture().oil_mix_viscosity(
            20.0, '16  ', '45', '100') == 17.67

    def test_oil_mix_viscosity_string_coma_input(self):
        assert OilMixture().oil_mix_viscosity(
            20, ' 16,0', '45,0', '100') == 17.67

    def test_mix_proportions(self):
        assert OilMixture().mix_proportions(
            680, 220, 460, '40') == (67.32, 32.68)

    def test_mix_proportions_string_input(self):
        assert OilMixture().mix_proportions(
            '680,0', '220 ', '460', '40') == (67.32, 32.68)

    @nose.tools.raises(ConceptError)
    def test_mix_proportions_wrong_mix_viscosity(self):
        OilMixture().mix_proportions(320, 680, '220', '40')

    @nose.tools.raises(ViscosityIntervalError)
    def test_mix_proportions_wrong_mix_viscosity1(self):
        OilMixture().mix_proportions(320, 680, '1000', '40')


class TestOilBlend:
    """Class to test OilBlend."""

    def test_additive_percent_mass(self):
        blend = OilBlend(additive_percent=8.0)
        assert blend.additive_percent_mass(additive_density=.959,
                                           oil_density=0.881) == 8.71

    def test_additive_percent_mass_string_input(self):
        blend = OilBlend(additive_percent='8.0')
        assert blend.additive_percent_mass(additive_density='0,959',
                                           oil_density=' 0.881') == 8.71

    def test_total_ash(self):
        blend = OilBlend(additive_percent=8.5)
        assert blend.total_ash(Calcium=0.47,
                               Magnesium=1.15,
                               zinc=1.66) == 0.83

    def test_total_ash_string_input(self):
        blend = OilBlend(additive_percent='8.5 ')
        assert blend.total_ash(Calcium='.47',
                               Magnesium=' 1,15',
                               zinc=1.66) == 0.83


class TestBearing:
    """Class to test Bearing class."""

    def test_grease_amount(self):
        """Test grease_amount()."""
        assert Bearing().grease_amount(25, 60) == 7.5

    def test_lubrication_frequency_float(self):
        """Test lubrication_frequency()."""
        assert Bearing().lubrication_frequency(rpm=1750.0,
                                               inner_diameter=18.0,
                                               ft=0,
                                               fc=1,
                                               fh=2,
                                               fv=0,
                                               fp=0,
                                               fd=2) == 508

    def test_lubrication_frequency_string(self):
        """Test lubrication_frequency()."""
        assert Bearing().lubrication_frequency(rpm='1750.0 ',
                                               inner_diameter='18,0',
                                               ft=0,
                                               fc=1,
                                               fh=2,
                                               fv=0,
                                               fp=0,
                                               fd=2) == 508

    def test_velocity_factor(self):
        """Test speed_factor()."""
        assert Bearing().velocity_factor(58, 45, 3000) == 154500

    @nose.tools.raises(ConceptError)
    def test_velocity_factor_inverted_diameters(self):
        """Test speed_factor()."""
        Bearing().velocity_factor(45, 60, 3000)


if __name__ == '__main__':
    nose.run()
