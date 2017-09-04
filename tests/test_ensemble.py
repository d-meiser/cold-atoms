import coldatoms
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


def arrays_close(x, y, epsilon=1.0e-6, tiny=1.0e-30):
    nrm_x = np.linalg.norm(x)
    nrm_y = np.linalg.norm(y)
    if nrm_x < tiny and nrm_y < tiny:
        return True
    normalization = nrm_x + nrm_y
    return (np.linalg.norm(x - y) / normalization) < epsilon


def check_json_roundtrip(ensemble):
    ensemble2 = coldatoms.json_to_ensemble(coldatoms.ensemble_to_json(ensemble))
    assert(arrays_close(ensemble.x, ensemble2.x))
    assert(arrays_close(ensemble.v, ensemble2.v))
    assert(set(ensemble.ensemble_properties.keys()) ==
           set(ensemble2.ensemble_properties.keys()))
    for k in ensemble.ensemble_properties.keys():
        assert(np.abs(ensemble.ensemble_properties[k] -
                      ensemble2.ensemble_properties[k]) < 1.0e-12)
    assert(set(ensemble.particle_properties.keys()) ==
           set(ensemble2.particle_properties.keys()))
    for k in ensemble.particle_properties.keys():
        assert(ensemble.particle_properties[k].shape ==
               ensemble2.particle_properties[k].shape)
        assert(arrays_close(ensemble.particle_properties[k],
                            ensemble2.particle_properties[k]))


def test_serialize_ensemble_rand_phase_space():
    num_ptcls = 120
    ensemble = coldatoms.Ensemble(num_ptcls)
    ensemble.x = np.random.random_sample(tuple(ensemble.x.shape))
    ensemble.v = np.random.random_sample(tuple(ensemble.v.shape))
    check_json_roundtrip(ensemble)


def test_serialize_ensemble_rand_phase_space_with_particle_props():
    num_ptcls = 120
    ensemble = coldatoms.Ensemble(num_ptcls)
    ensemble.x = np.random.random_sample(tuple(ensemble.x.shape))
    ensemble.v = np.random.random_sample(tuple(ensemble.v.shape))
    ensemble.particle_properties['mass'] = (
        np.random.random_sample(ensemble.x.shape[0]))
    ensemble.particle_properties['density_matrix'] = (
        np.random.random_sample((ensemble.x.shape[0], 4, 4)))
    check_json_roundtrip(ensemble)


def test_serialize_ensemble_rand_phase_space_with_ensemble_props():
    num_ptcls = 2
    ensemble = coldatoms.Ensemble(num_ptcls)
    ensemble.x = np.random.random_sample(tuple(ensemble.x.shape))
    ensemble.v = np.random.random_sample(tuple(ensemble.v.shape))
    ensemble.ensemble_properties['mass'] = 100.0
    check_json_roundtrip(ensemble)


#def test_serialize_ensemble():
#    num_ptcls = 12
#    ensemble = coldatoms.Ensemble(num_ptcls)
#    ensemble.x = np.random.random_sample(tuple(ensemble.x.shape))
#    ensemble.v = np.random.random_sample(tuple(ensemble.v.shape))
#    ensemble.particle_properties['mass'] = (
#        np.random.random_sample(ensemble.x.shape[0]))
#    ensemble.particle_properties['density_matrix'] = (
#        np.random.random_sample((ensemble.x.shape[0], 4, 4)))
#    ensemble.ensemble_properties['charge'] = 1.7
#    check_json_roundtrip(ensemble)
#
