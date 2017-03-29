from .context import coldatoms
import numpy as np
from nose.tools import *


class test_coulomb(object):

    def setup(self):
        self.coulomb_force = coldatoms.CoulombForce()
        self.ensemble = coldatoms.Ensemble(num_ptcls=3)
        self.ensemble.x[1] = np.array([1.0, 1.0, 1.0])
        self.ensemble.x[2] = np.array([2.0, 2.0, 2.0])
        self.ensemble.ensemble_properties['charge'] = 1.0

    @raises(Exception)
    def test_must_provide_charge(self):
        self.ensemble.ensemble_properties = {}
        self.coulomb_force.force(1.0e-1, self.ensemble)

    def test_can_call_with_ensemble_charge(self):
        self.ensemble.ensemble_properties['charge'] = 1.0
        self.coulomb_force.force(1.0e-1, self.ensemble)

    def test_can_call_with_per_particle_charge(self):
        charges = np.ones(3)
        self.ensemble.ensemble_properties = {}
        self.ensemble.set_particle_property('charge', charges)
        self.coulomb_force.force(1.0e-1, self.ensemble)

    def test_force_between_like_charges_is_repulsive(self):
        f = self.coulomb_force.force(1.0e-1, self.ensemble)
        assert(f[0, 0] < 0)
        assert(f[0, 1] < 0)
        assert(f[0, 2] < 0)

    def test_force_between_opposite_charges_is_attractive(self):
        charges = np.ones(3)
        charges[1] = -1.0
        self.ensemble.set_particle_property('charge', charges)
        self.ensemble.ensemble_properties = {}
        self.ensemble.x[2] = np.array([100.0, 100.0, 100.0])
        f = self.coulomb_force.force(1.0e-1, self.ensemble)
        assert(f[0, 0] > 0)
        assert(f[0, 1] > 0)
        assert(f[0, 2] > 0)

    def test_increasing_the_softcore_radius_decreases_force(self):
        f = self.coulomb_force.force(1.0e-1, self.ensemble)
        self.coulomb_force.delta = 1.0
        f_softcore = self.coulomb_force.force(1.0e-1, self.ensemble)
        assert(np.linalg.norm(f_softcore) < np.linalg.norm(f))

    def test_can_evaluate_force_for_particles_in_same_position(self):
        self.ensemble.x[1] = np.zeros(3)
        f = self.coulomb_force.force(1.0e-1, self.ensemble)
