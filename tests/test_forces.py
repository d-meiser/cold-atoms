import coldatoms
import numpy as np

# Some integration tests for force evaluation

class tests(object):

    def setup(self):
        self.kx = 2.0
        self.ky = 3.0
        self.kz = -1.0
        self.coulomb = coldatoms.CoulombForce()
        self.harmonic_trap = coldatoms.HarmonicTrapPotential(self.kx, self.ky, self.kz)
        self.ensemble = coldatoms.Ensemble(num_ptcls=3)
        self.ensemble.x[1] = np.array([1.0, 1.0, 1.0])
        self.ensemble.x[2] = np.array([2.0, 2.0, 2.0])
        self.ensemble.ensemble_properties['charge'] = 1.0

    def tests_commute(self):
        dt = 1.3e-3

        fab = np.zeros_like(self.ensemble.v)
        self.coulomb.force(dt, self.ensemble, fab)
        self.harmonic_trap.force(dt, self.ensemble, fab)

        fba = np.zeros_like(self.ensemble.v)
        self.harmonic_trap.force(dt, self.ensemble, fba)
        self.coulomb.force(dt, self.ensemble, fba)

        normalization = np.linalg.norm(fab) + np.linalg.norm(fba)
        assert(np.linalg.norm(fab - fba) / normalization < 1.0e-5)

