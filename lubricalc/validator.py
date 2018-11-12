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
    def validate_float(name, value):
        """Validate input value as float."""
        value = str(value).replace(',', '.').strip()
        try:
            value = float(value)
        except ValueError:
            raise ValueError('{0}: Input value must be a valid number, '
                             'not {1}'.format(name, value))

        if value == float('inf'):
            raise ValueError('{0}: Input value must be a valid number, '
                             'not infinite value'.format(name))

        return value

    @staticmethod
    def validate_lower_limit(name, value, limit=0):
        """Validate value is greater than a given value (limit)."""
        if value <= limit:
            raise ConceptError('{0}: Input value must be '
                               'greater than {1}'.format(name, limit))