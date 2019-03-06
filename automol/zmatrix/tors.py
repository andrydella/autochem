""" functions for working with torsional degrees of freedom
"""
import numpy
from ..graph import bond_symmetry_numbers as _bond_symmetry_numbers
from ._graph import connectivity_graph as _connectivity_graph
from ._core import set_values as _set_values
from ._core import dihedral_keys as _dihedral_keys
from ._core import dihedral_names as _dihedral_names


def symmetry_numbers(zma, tors_names):
    """ symmetry numbers for torsional dihedrals
    """
    dih_edg_key_dct = _dihedral_edge_keys(zma)
    assert set(tors_names) <= set(dih_edg_key_dct.keys())
    edg_keys = tuple(map(dih_edg_key_dct.__getitem__, tors_names))

    gra = _connectivity_graph(zma)
    bnd_sym_num_dct = _bond_symmetry_numbers(gra)
    assert set(edg_keys) <= set(bnd_sym_num_dct.keys())

    tors_sym_nums = tuple(map(bnd_sym_num_dct.__getitem__, edg_keys))
    return tors_sym_nums


def samples(zma, nsamp, tors_names, tors_ranges=None):
    """ randomly sample over torsional dihedrals
    """
    if tors_ranges is None:
        sym_nums = symmetry_numbers(zma, tors_names)
        tors_ranges = [(0, 2*numpy.pi/sym_num) for sym_num in sym_nums]

    tors_vals_lst = _sample_ranges(tors_ranges, nsamp)

    zmas = tuple(_set_values(zma, dict(zip(tors_names, tors_vals)))
                 for tors_vals in tors_vals_lst)
    return zmas


def _dihedral_edge_keys(zma):
    """ dihedral bonds, by name
    """
    dih_names = _dihedral_names(zma)
    dih_keys = _dihedral_keys(zma)
    dih_edg_key_dct = {dih_name: frozenset(dih_key[1:3])
                       for dih_name, dih_key in zip(dih_names, dih_keys)}
    return dih_edg_key_dct


def _sample_ranges(ranges, nsamp):
    """ randomly sample over several ranges
    """
    nrange = len(ranges)
    samp_mat = numpy.random.rand(nsamp, nrange)
    for i, (start, stop) in enumerate(ranges):
        samp_mat[:, i] = samp_mat[:, i] * (stop - start) + start
    return tuple(map(tuple, samp_mat))
