#!/usr/bin/env python
#*****************************************************************************
#       Copyright (C) 2020 Vincent Delecroix <20100.delecroix@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
#*****************************************************************************

import sys
import pytest

from surface_dynamics import AbelianStratum

def representative(cd):
    return min([cd.canonical_label(), cd.horizontal_symmetry().canonical_label(), cd.vertical_symmetry().canonical_label(), cd.inverse().canonical_label()])

def match_list_up_to_symmetry(A, k):
    cds_compute = A.cylinder_diagrams(k, True, True)
    cds_database = A.cylinder_diagrams(k, True, False)

    assert len(cds_compute) == len(cds_database)
    assert len(cds_compute) == A.cylinder_diagrams_number(k, True, True)
    assert len(cds_compute) == A.cylinder_diagrams_number(k, True, False)

    cds_compute = [representative(cd) for cd in cds_compute]
    cds_database = [representative(cd) for cd in cds_database]
    cds_compute.sort()
    cds_database.sort()

    assert cds_compute == cds_database

    assert len(set(cds_compute)) == len(cds_database)

def match_list_no_symmetry(A, k):
    cds_compute = A.cylinder_diagrams(k, False, True)
    cds_database = A.cylinder_diagrams(k, False, False)

    assert len(cds_compute) == len(cds_database)
    assert len(cds_compute) == A.cylinder_diagrams_number(k, False, True)
    assert len(cds_compute) == A.cylinder_diagrams_number(k, False, False)

    cds_compute = [cd.canonical_label(inplace=False) for cd in cds_compute]
    cds_database = [cd.canonical_label(inplace=False) for cd in cds_database]
    cds_compute.sort()
    cds_database.sort()

    assert cds_compute == cds_database

    assert len(set(cds_compute)) == len(cds_database)

def cylinder_diagrams_testing(A):
    ccs = A.components()
    d = A.genus() + A.nb_zeros() - 1

    for k in range(1, d + 1):
        match_list_up_to_symmetry(A, k)
        match_list_no_symmetry(A, k)

        for cc in A.components():
            match_list_up_to_symmetry(cc, k)
            match_list_no_symmetry(cc, k)

def test_H2():
    cylinder_diagrams_testing(AbelianStratum(2))

def test_H11():
    cylinder_diagrams_testing(AbelianStratum(1,1))

def test_H4():
    cylinder_diagrams_testing(AbelianStratum(4))

def test_H22():
    cylinder_diagrams_testing(AbelianStratum(2,2))

def test_H31():
    cylinder_diagrams_testing(AbelianStratum(3,1))

def test_H6():
    cylinder_diagrams_testing(AbelianStratum(6))

def test_H211():
    cylinder_diagrams_testing(AbelianStratum(2,1,1))

if __name__ == '__main__': sys.exit(pytest.main(sys.argv))