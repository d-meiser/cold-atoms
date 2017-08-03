import coldatoms
import numpy as np


class test_advance(object):

    def setup(self):
        self.ensemble = coldatoms.Ensemble(num_ptcls=3)
        self.ensemble.x[1] = np.array([1.0, 1.0, 1.0])
        self.ensemble.x[2] = np.array([2.0, 2.0, 2.0])
        self.ensemble.ensemble_properties['charge'] = 1.0

    def test_identity_advance(self):
        initial_ensemble = self.ensemble.copy()
        coldatoms.advance(self.ensemble)
        assert(initial_ensemble.equal(self.ensemble))


