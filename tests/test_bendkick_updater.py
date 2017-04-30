import coldatoms
import numpy as np


class test_bendkickupdater(object):

    def setup(self):
        self.ensemble = coldatoms.Ensemble(num_ptcls=1)
        self.ensemble.v[0] = np.array([1.0, 0.0, 0.0])
        self.ensemble.ensemble_properties['charge'] = 3.3
        self.ensemble.ensemble_properties['mass'] = 2.7

    def test_near_zero_field(self):
        Bz = 1.0e-30
        dt = 1.0

        expected_position =  self.ensemble.x[0] + dt * self.ensemble.v[0]
        expected_velocity = self.ensemble.v[0]

        coldatoms.bend_kick(dt, Bz, self.ensemble, [])

        assert(np.linalg.norm(self.ensemble.x[0] - expected_position) < 1.0e-8)
        assert(np.linalg.norm(self.ensemble.v[0] - expected_velocity) < 1.0e-8)

    def test_closed_circle(self):
        Bz = 1.0
        q = self.ensemble.ensemble_properties['charge']
        m = self.ensemble.ensemble_properties['mass']
        omegaB = Bz * q / m
        dt = 2.0 * np.pi / omegaB

        expected_position =  self.ensemble.x[0]
        expected_velocity = self.ensemble.v[0]

        coldatoms.bend_kick(dt, Bz, self.ensemble, [])

        assert(np.linalg.norm(self.ensemble.x[0] - expected_position) < 1.0e-8)
        assert(np.linalg.norm(self.ensemble.v[0] - expected_velocity) < 1.0e-8)

    def test_force_gets_called(self):
        Bz = 1.0e-30
        dt = 1.0

        class MockForce(object):
            def force(self, dt, ensemble, f):
                self.position = np.copy(ensemble.x)

        expected_position =  self.ensemble.x[0] + 0.5 * dt * self.ensemble.v[0]

        force = MockForce()

        coldatoms.bend_kick(dt, Bz, self.ensemble, [force])

        assert(np.linalg.norm(force.position - expected_position) < 1.0e-8)

