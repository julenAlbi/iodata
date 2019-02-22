# -*- coding: utf-8 -*-
# IODATA is an input and output module for quantum chemistry.
#
# Copyright (C) 2011-2019 The IODATA Development Team
#
# This file is part of IODATA.
#
# IODATA is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# IODATA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --
# pragma pylint: disable=invalid-name
"""Test iodata.cube module."""


import numpy as np

from .. iodata import IOData

try:
    from importlib_resources import path
except ImportError:
    from importlib.resources import path


def test_load_aelta():
    with path('iodata.test.data', 'aelta.cube') as fn_cube:
        mol = IOData.from_file(str(fn_cube))
    assert mol.title == 'Some random cube for testing (sort of) useless data'
    assert mol.natom == 72
    assert abs(mol.coordinates[5, 0] - 27.275511) < 1e-5
    assert abs(mol.coordinates[-2, 2] - 26.460812) < 1e-5
    assert (mol.grid['shape'] == 12).all()
    rvecs = mol.cell
    my_rvecs = np.array([[1.8626, 0.1, 0.0], [0.0, 1.8626, 0.0], [0.0, 0.0, 1.8626]], float) * 12
    assert abs(rvecs - my_rvecs).max() < 1e-5
    rvecs = mol.grid['grid_rvecs']
    my_rvecs = np.array([[1.8626, 0.1, 0.0], [0.0, 1.8626, 0.0], [0.0, 0.0, 1.8626]], float)
    assert abs(rvecs - my_rvecs).max() < 1e-5
    assert abs(mol.grid['origin'] - np.array([0.0, 1.2, 0.0])).max() < 1e-10
    assert abs(mol.cube_data[0, 0, 0] - 9.49232e-06) < 1e-12
    assert abs(mol.cube_data[-1, -1, -1] - 2.09856e-04) < 1e-10
    pn = mol.pseudo_numbers
    assert abs(pn[0] - 1.0) < 1e-10
    assert abs(pn[1] - 0.1) < 1e-10
    assert abs(pn[-2] - 0.2) < 1e-10
    assert abs(pn[-1] - mol.numbers[-1]) < 1e-10


def test_load_dump_load_aelta(tmpdir):
    with path('iodata.test.data', 'aelta.cube') as fn_cube1:
        mol1 = IOData.from_file(str(fn_cube1))

    fn_cube2 = '%s/%s' % (tmpdir, 'aelta.cube')
    mol1.to_file(fn_cube2)
    mol2 = IOData.from_file(fn_cube2)

    assert mol1.title == mol2.title
    assert abs(mol1.coordinates - mol2.coordinates).max() < 1e-4
    assert (mol1.numbers == mol2.numbers).all()
    ugrid1 = mol1.grid
    ugrid2 = mol2.grid
    assert abs(ugrid1["grid_rvecs"] - ugrid2["grid_rvecs"]).max() < 1e-4
    assert (ugrid1["shape"] == ugrid2["shape"]).all()
    assert abs(mol1.cube_data - mol2.cube_data).max() < 1e-4
    assert abs(mol1.pseudo_numbers - mol2.pseudo_numbers).max() < 1e-4
