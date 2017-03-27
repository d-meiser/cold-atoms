from .context import coldatoms
import numpy as np
from nose.tools import *


def test_create_coulomb_force():
    f = coldatoms.CoulombForce()


@raises(Exception)
def test_must_provide_charge():
    ensemble = coldatoms.Ensemble(num_ptcls=3)
    f = coldatoms.CoulombForce()
    f.force(1.0e-1, ensemble)


def test_can_call_with_ensemble_charge():
    ensemble = coldatoms.Ensemble(num_ptcls=3)
    ensemble.x[1] = np.array([1.0, 1.0, 1.0])
    ensemble.x[2] = np.array([2.0, 2.0, 2.0])
    ensemble.ensemble_properties['charge'] = 1.0
    f = coldatoms.CoulombForce()
    f.force(1.0e-1, ensemble)
