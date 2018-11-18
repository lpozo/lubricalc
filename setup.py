#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: setup.py
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

"""This module provides a setup.py script for AddressBook app."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from lubricalc.config import DESC
from lubricalc.config import LONG_DESC


if __name__ == '__main__':
    setup(name='Lubricalc',
          version='0.1',
          description=DESC,
          long_description=LONG_DESC,
          author='Leodanis Pozo Ramos',
          author_email='lpozor78@gmail.com',
          maintainer='Leodanis Pozo Ramos',
          maintainer_email='lpozor78@gmail.com',
          url='https://github.com/lpozo/lubricalc',
          license='GNU General Public License, Version 2, June 1991',
          platforms=['linux', 'win32'],
          scripts=['bin/lubricalc'],
          py_modules=['main', 'controller'],
          packages=['lubricalc'],
          data_files=[('share/applications/Lubricalc',
                       ['AUTHORS', 'LICENSE',
                        'screenshot.png, requirements.txt'])],
          keywords='machinery lubrication, oil, grease, lubrication engineering',
    )
