# -*- coding: utf-8 -*-
# Horton is a Density Functional Theory program.
# Copyright (C) 2011-2013 Toon Verstraelen <Toon.Verstraelen@UGent.be>
#
# This file is part of Horton.
#
# Horton is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Horton is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
#--


import numpy as np
from horton import *


def test_unravel_counter():
    from horton.io.vasp import unravel_counter
    assert unravel_counter(0, [3, 3, 3]) == [0, 0, 0]
    assert unravel_counter(0, [2, 4, 3]) == [0, 0, 0]
    assert unravel_counter(1, [2, 4, 3]) == [1, 0, 0]
    assert unravel_counter(2, [2, 4, 3]) == [0, 1, 0]
    assert unravel_counter(3, [2, 4, 3]) == [1, 1, 0]
    assert unravel_counter(8, [2, 4, 3]) == [0, 0, 1]
    assert unravel_counter(9, [2, 4, 3]) == [1, 0, 1]
    assert unravel_counter(11, [2, 4, 3]) == [1, 1, 1]
    assert unravel_counter(24, [2, 4, 3]) == [0, 0, 0]


def test_load_chgcar_oxygen():
    fn = context.get_fn('test/CHGCAR.oxygen')
    sys = System.from_file(fn)
    assert sys.natom == 1
    assert (sys.numbers == 8).all()
    assert abs(sys.cell.volume - (10*angstrom)**3) < 1e-10
    ui_grid = sys.props['ui_grid']
    assert len(ui_grid.shape) == 3
    assert (ui_grid.shape == 2).all()
    assert abs(ui_grid.grid_cell.rvecs - sys.cell.rvecs/2).max() < 1e-10
    assert abs(ui_grid.origin).max() < 1e-10
    d = sys.props['cube_data']
    assert abs(d[0,0,0] - 0.78406017013E+04/sys.cell.volume) < 1e-10
    assert abs(d[-1,-1,-1] - 0.10024522914E+04/sys.cell.volume) < 1e-10
    assert abs(d[1,0,0] - 0.76183317989E+04/sys.cell.volume) < 1e-10


def test_load_chgcar_water():
    fn = context.get_fn('test/CHGCAR.water')
    sys = System.from_file(fn)
    assert sys.natom == 3
    assert (sys.numbers == np.array([8, 1, 1])).all()
    assert abs(sys.coordinates[1] - np.array([0.074983,  0.903122,  0.000000])*15*angstrom).max() < 1e-10
    assert abs(sys.cell.volume - (15*angstrom)**3) < 1e-10
    ui_grid = sys.props['ui_grid']
    assert len(ui_grid.shape) == 3
    assert (ui_grid.shape == 3).all()
    assert abs(ui_grid.grid_cell.rvecs - sys.cell.rvecs/3).max() < 1e-10
    assert abs(ui_grid.origin).max() < 1e-10


def test_load_locpot_oxygen():
    fn = context.get_fn('test/LOCPOT.oxygen')
    sys = System.from_file(fn)
    assert sys.natom == 1
    assert sys.numbers[0] == 8
    assert abs(sys.cell.volume - (10*angstrom)**3) < 1e-10
    ui_grid = sys.props['ui_grid']
    assert len(ui_grid.shape) == 3
    assert (ui_grid.shape == [1, 4, 2]).all()
    assert abs(ui_grid.origin).max() < 1e-10
    d = sys.props['cube_data']
    assert abs(d[0, 0, 0]/electronvolt - 0.35046350435E+01) < 1e-10
    assert abs(d[0, 1, 0]/electronvolt - 0.213732132354E+01) < 1e-10
    assert abs(d[0, 2, 0]/electronvolt - -.65465465497E+01) < 1e-10
    assert abs(d[0, 2, 1]/electronvolt - -.546876467887E+01) < 1e-10


def test_load_poscar_water():
    fn = context.get_fn('test/POSCAR.water')
    sys = System.from_file(fn)
    assert sys.natom == 3
    assert (sys.numbers == np.array([8, 1, 1])).all()
    assert abs(sys.coordinates[1] - np.array([0.074983,  0.903122,  0.000000])*15*angstrom).max() < 1e-10
    assert abs(sys.cell.volume - (15*angstrom)**3) < 1e-10
