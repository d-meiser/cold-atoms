from .context import coldatoms
import numpy as np
from nose.tools import *


def test_no_sources_produce_no_particles():
    ensemble = coldatoms.Ensemble(num_ptcls=17)
    coldatoms.produce_ptcls(1.0, ensemble, [])
    assert(ensemble.num_ptcls == 17)


class TrivialSource(coldatoms.Source):
    num_ptcls = 10

    def num_ptcls_produced(self, dt):
        return TrivialSource.num_ptcls

    def produce_ptcls(self, dt, start, end, ensemble):
        for i in range(start, end):
            ensemble.x[i, 0] = i


def test_when_there_is_a_source_the_ensemble_size_grows():
    ensemble = coldatoms.Ensemble(num_ptcls=17)
    s = TrivialSource()
    coldatoms.produce_ptcls(1.0, ensemble, [s])
    assert(ensemble.num_ptcls > 17)


def test_positions_get_generated():
    ensemble = coldatoms.Ensemble(num_ptcls=17)
    s = TrivialSource()
    coldatoms.produce_ptcls(1.0, ensemble, [s])
    for i in range(17, ensemble.num_ptcls):
        assert(abs(ensemble.x[i, 0] - i) < 1.0e-6)


def test_can_use_multiple_sources():
    ensemble = coldatoms.Ensemble(num_ptcls=17)
    s = TrivialSource()
    coldatoms.produce_ptcls(3.0, ensemble, [s, s])

    assert(ensemble.num_ptcls == 17 + 2 * s.num_ptcls_produced(1.0))

    for i in range(17,  ensemble.num_ptcls):
        assert(abs(ensemble.x[i, 0] - i) < 1.0e-6)



