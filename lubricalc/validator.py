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
            if value == '':
                value = 'null'
            raise ValueError('{0}: Input value must be a valid number, '
                             'not: {1}'.format(name, value))

        if value in (float('inf'), float('-inf')):
            raise ValueError('{0}: Input value must be a valid number, '
                             'not: infinite'.format(name))

        return value

    @staticmethod
    def validate_lower_limit(name, value, limit=0, strict=False):
        """Validate value is greater than a given value (limit)."""
        if not strict:
            if value < limit:
                raise ConceptError('{0}: Input value must be '
                                   'greater than or equal to {1}'.format(
                                        name, limit))
        else:
            if value <= limit:
                raise ConceptError('{0}: Input value must be '
                                   'greater than {1}'.format(name, limit))


def validate(obj, name, value, attr, limit=0, strict=False):
    """Validate and set attributes of an object."""
    validator = Validator()
    value = validator.validate_float(name, value)
    lower_limit = limit
    validator.validate_lower_limit(name, value, lower_limit, strict)
    setattr(obj, attr, value)


class Float:
    """Descriptor for representing float values."""

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        """Validate input value as float."""
        value = str(value).replace(',', '.').strip()
        try:
            value = float(value)
        except ValueError:
            raise ValueError('Input value must be a valid float number')

        if value in (float('inf'), float('-inf')):
            raise ValueError('Input value must be a valid float number')

        self._value = value


class NonZeroPositiveFloat:
    """Descriptor for representing non-zero positive values."""

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        """Validate input value as float."""
        self.__value = value
        if self.__value <= 0:
            raise ValueError('Input value must be greater than 0')

        self._value = self.__value

    __value = Float()


class Viscosity:
    """Descriptor for representing viscosity values."""

    def __get__(self, instance, owner):
        return self._viscosity

    def __set__(self, instance, value):
        self.__viscosity = value
        if self.__viscosity < 2:
            raise ConceptError('Viscosity must be greater or equal to 2')

        self._viscosity = self.__viscosity

    __viscosity = Float()


class ViscosityIndex:
    """Descriptor for representing viscosity index values."""

    def __get__(self, instance, owner):
        return self._index

    def __set__(self, instance, value):
        if value < 0.0 or value > 400.0:
            raise ConceptError('Viscosity Index must be between 0 and 400')

        self._index = value


class Temperature:
    """Descriptor for representing non-zero positive values."""

    def __get__(self, instance, owner):
        return self._temperature

    def __set__(self, instance, value):
        self.__temperature = value
        if self.__temperature >= -50:
            self._temperature = self.__temperature
        else:
            raise ConceptError('Temperature must be greater -50°C')

    __temperature = Float()
