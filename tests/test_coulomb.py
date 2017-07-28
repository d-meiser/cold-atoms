import coldatoms
import numpy as np
from nose.tools import *


class test_coulomb(object):

    def setup(self):
        self.coulomb_force = coldatoms.CoulombForce()
        self.ensemble = coldatoms.Ensemble(num_ptcls=3)
        self.ensemble.x[1] = np.array([1.0, 1.0, 1.0])
        self.ensemble.x[2] = np.array([2.0, 2.0, 2.0])
        self.ensemble.ensemble_properties['charge'] = 1.0
        self.f = np.zeros_like(self.ensemble.v)

    @raises(Exception)
    def test_must_provide_charge(self):
        self.ensemble.ensemble_properties = {}
        self.coulomb_force.force(1.0e-1, self.ensemble, self.f)

    def test_can_call_with_ensemble_charge(self):
        self.ensemble.ensemble_properties['charge'] = 1.0
        self.coulomb_force.force(1.0e-1, self.ensemble, self.f)

    def test_can_call_with_per_particle_charge(self):
        charges = np.ones(3)
        self.ensemble.ensemble_properties = {}
        self.ensemble.set_particle_property('charge', charges)
        self.coulomb_force.force(1.0e-1, self.ensemble, self.f)

    def test_force_between_like_charges_is_repulsive(self):
        self.coulomb_force.force(1.0e-1, self.ensemble, self.f)
        assert(self.f[0, 0] < 0)
        assert(self.f[0, 1] < 0)
        assert(self.f[0, 2] < 0)

    def test_force_between_opposite_charges_is_attractive(self):
        charges = np.ones(3)
        charges[1] = -1.0
        self.ensemble.set_particle_property('charge', charges)
        self.ensemble.ensemble_properties = {}
        self.ensemble.x[2] = np.array([100.0, 100.0, 100.0])
        self.coulomb_force.force(1.0e-1, self.ensemble, self.f)
        assert(self.f[0, 0] > 0)
        assert(self.f[0, 1] > 0)
        assert(self.f[0, 2] > 0)

    def test_increasing_the_softcore_radius_decreases_force(self):
        self.coulomb_force.force(1.0e-1, self.ensemble, self.f)
        f = np.copy(self.f)
        self.f.fill(0.0)
        self.coulomb_force.delta = 1.0
        self.coulomb_force.force(1.0e-1, self.ensemble, self.f)
        f_softcore = np.copy(self.f)
        assert(np.linalg.norm(f_softcore) < np.linalg.norm(f))

    def test_can_evaluate_force_for_particles_in_same_position(self):
        self.ensemble.x[1] = np.zeros(3)
        self.coulomb_force.force(1.0e-1, self.ensemble, self.f)

    def test_compare_with_reference_impl(self):
        m, n = self.ensemble.x.shape
        self.ensemble.x = np.random.rand(m, n)
        self.coulomb_force.force(1.0e-2, self.ensemble, self.f)
        f = np.copy(self.f)
        self.f.fill(0.0)
        self.coulomb_force.use_reference_implementations()
        self.coulomb_force.force(1.0e-2, self.ensemble, self.f)
        f_ref = np.copy(self.f)
        normalization = np.linalg.norm(f_ref) + np.linalg.norm(f)
        assert(np.linalg.norm(f - f_ref) < 1.0e-9 * normalization)

    def test_per_particle_charge_spot_check(self):
        self.ensemble = coldatoms.Ensemble(2)
        self.ensemble.x[0, :] = 0.0
        self.ensemble.x[1, 0] = 1.3
        self.ensemble.x[1, 1] = 1.5
        self.ensemble.x[1, 2] = 1.7
        q = 1.3 * np.array([1.6e-19, 2.0 * 1.6e-19])
        self.ensemble.ensemble_properties = {}
        self.ensemble.set_particle_property('charge', q)
        dt = 1.0e-2
        r = self.ensemble.x[0, :] - self.ensemble.x[1, :]
        dist = np.linalg.norm(r)
        ke = 1.0 / (4.0 * np.pi * 8.854e-12)
        f_expected = ke * r * q[0] * q[1] / (dist**3)
        f_expected *= dt
        self.coulomb_force.force(dt, self.ensemble, self.f)
        normalization = np.sqrt(
            np.linalg.norm(self.f[0])**2 + np.linalg.norm(f_expected)**2)
        assert(np.linalg.norm(self.f[0] - f_expected) / normalization < 1.0e-9)

    def test_spot_check(self):
        self.ensemble = coldatoms.Ensemble(2)
        self.ensemble.x[0, :] = 0.0
        self.ensemble.x[1, 0] = 1.3
        self.ensemble.x[1, 1] = 1.5
        self.ensemble.x[1, 2] = 1.7
        q = 1.3
        self.ensemble.ensemble_properties['charge'] = q
        dt = 1.0e-2
        r = self.ensemble.x[0, :] - self.ensemble.x[1, :]
        dist = np.linalg.norm(r)
        ke = 1.0 / (4.0 * np.pi * 8.854e-12)
        f_expected = ke * r * q * q / (dist**3)
        f_expected *= dt
        self.coulomb_force.force(dt, self.ensemble, self.f)
        normalization = np.sqrt(
            np.linalg.norm(self.f[0])**2 + np.linalg.norm(f_expected)**2)
        assert(np.linalg.norm(self.f[0] - f_expected) / normalization < 1.0e-9)

    def test_compare_per_particle_charge_algs_with_reference_impl(self):
        m, n = self.ensemble.x.shape
        self.ensemble.x = np.random.rand(m, n)
        q = np.random.rand(m)
        self.ensemble.set_particle_property('charge', q)
        self.ensemble.ensemble_properties = {}
        self.coulomb_force.force(1.0e-2, self.ensemble, self.f)
        f = np.copy(self.f)
        self.f.fill(0.0)
        self.coulomb_force.use_reference_implementations()
        self.coulomb_force.force(1.0e-2, self.ensemble, self.f)
        f_ref = np.copy(self.f)
        normalization = np.linalg.norm(f_ref) + np.linalg.norm(f)
        assert(np.linalg.norm(f - f_ref) < 1.0e-9 * normalization)

    def test_compare_with_reference_impl_large_num_ptcls(self):
        self.ensemble.x = np.zeros([100, 3])
        m, n = self.ensemble.x.shape
        self.ensemble.x = np.random.rand(m, n)
        self.f = np.zeros_like(self.ensemble.x)
        self.coulomb_force.force(1.0e-2, self.ensemble, self.f)
        f = np.copy(self.f)
        self.f.fill(0.0)
        self.coulomb_force.use_reference_implementations()
        self.coulomb_force.force(1.0e-2, self.ensemble, self.f)
        f_ref = np.copy(self.f)
        normalization = np.linalg.norm(f_ref) + np.linalg.norm(f)
        assert(np.linalg.norm(f - f_ref) < 1.0e-9 * normalization)
