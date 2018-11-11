# -*- coding: utf-8 -*-

# File name: validator.py
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

"""This module provides Data Validator Class."""

from .exception import *


class Validator:
    """Data validation class."""

    @staticmethod
    def validate_float(value):
        """Validate input value as float."""
        value = str(value).replace(',', '.').strip()
        try:
            value = float(value)
        except ValueError:
            raise ValueError('Input value must be a valid number, '
                             'not {v}'.format(v=value))

        if value == float('inf'):
            raise ValueError('Input value must be a valid number, '
                             'not infinite value')

        return value

    @staticmethod
    def validate_lower_limit(value, limit=0):
        """Validate value is greater than a given value (limit)."""
        if value <= limit:
            raise ConceptError('Input value must be '
                               'greater than {l}'.format_map(l=limit))

    def validate_viscosity(self, *data):
        for datum in data:
            if datum < 2:
                raise TooLowViscosityError('Input value is a concept error')

