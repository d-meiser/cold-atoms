import coldatoms
import numpy as np
from nose.tools import *


class test_harmonic_trap_forces(object):

    def setup(self):
        self.kx = 2.0
        self.ky = 3.0
        self.kz = -1.0
        self.harmonic_trap_force = coldatoms.HarmonicTrapPotential(self.kx, self.ky, self.kz)
        self.num_ptcls = 5
        self.ensemble = coldatoms.Ensemble(num_ptcls=self.num_ptcls)
        self.ensemble.x[:, 0] = np.random.random(self.num_ptcls)
        self.ensemble.x[:, 1] = np.random.random(self.num_ptcls)
        self.ensemble.x[:, 2] = np.random.random(self.num_ptcls)
        self.ensemble.ensemble_properties['charge'] = 1.0
        self.f = np.zeros_like(self.ensemble.v)

    @raises(Exception)
    def test_must_provide_charge(self):
        self.ensemble.ensemble_properties = {}
        self.harmonic_trap_force.force(1.0e-1, self.ensemble, self.f)

    def test_can_call_with_ensemble_charge(self):
        self.ensemble.ensemble_properties['charge'] = 1.0
        self.harmonic_trap_force.force(1.0e-1, self.ensemble, self.f)

    def test_can_call_with_per_particle_charge(self):
        charges = np.ones(self.num_ptcls)
        self.ensemble.ensemble_properties = {}
        self.ensemble.set_particle_property('charge', charges)
        self.harmonic_trap_force.force(1.0e-1, self.ensemble, self.f)

    def test_compare_with_reference_impl_large_num_ptcls(self):
        self.ensemble.x = np.zeros([100, 3])
        m, n = self.ensemble.x.shape
        self.ensemble.x = np.random.rand(m, n)
        self.f = np.zeros_like(self.ensemble.x)
        self.harmonic_trap_force.force(1.0e-2, self.ensemble, self.f)
        f = np.copy(self.f)
        self.f.fill(0.0)
        self.harmonic_trap_force.use_reference_implementations()
        self.harmonic_trap_force.force(1.0e-2, self.ensemble, self.f)
        f_ref = np.copy(self.f)
        normalization = np.linalg.norm(f_ref) + np.linalg.norm(f)
        assert(np.linalg.norm(f - f_ref) < 1.0e-9 * normalization)
