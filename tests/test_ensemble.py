from .context import coldatoms
import numpy as np
import math
from nose.tools import *


def test_construct_ensemble():
    ensemble = coldatoms.Ensemble()


def test_default_number_of_ptcls_is_one():
    ensemble = coldatoms.Ensemble()
    assert(ensemble.num_ptcls == 1)


def test_num_ptcls_can_be_overridden():
    ensemble = coldatoms.Ensemble(num_ptcls=11)
    assert(ensemble.num_ptcls == 11)


def test_array_sizes_consistent_with_num_ptcls():
    ensemble = coldatoms.Ensemble(40)
    assert(ensemble.num_ptcls == ensemble.x.shape[0])
    assert(ensemble.num_ptcls == ensemble.v.shape[0])


def test_can_set_ensemble_property():
    ensemble = coldatoms.Ensemble(20)
    ensemble.ensemble_properties['mass'] = 87.0


def test_can_set_particle_property():
    ensemble = coldatoms.Ensemble(20)
    ensemble.set_particle_property('mass', np.ones_like(ensemble.x))
    mass = ensemble.particle_properties['mass']
    assert(mass.shape[0] == ensemble.num_ptcls)


@raises(Exception)
def test_bad_shape_of_particle_props_raises_exception():
    ensemble = coldatoms.Ensemble(10)
    ensemble.set_particle_property('mass', np.ones(12))


def test_can_grow():
    ensemble = coldatoms.Ensemble(12)
    new_size = 15
    ensemble.resize(new_size)
    assert(ensemble.num_ptcls == new_size)


def test_can_shrink():
    ensemble = coldatoms.Ensemble(12)
    new_size = 9
    ensemble.resize(new_size)
    assert(ensemble.num_ptcls == new_size)

def test_can_resize_with_particle_props():
    ensemble = coldatoms.Ensemble(12)
    ensemble.set_particle_property('mass', np.ones(12))
    new_size = 15
    ensemble.resize(new_size)
    assert(ensemble.num_ptcls == new_size)
    assert(ensemble.particle_properties['mass'].shape[0] == new_size)
