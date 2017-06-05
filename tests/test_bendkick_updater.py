import coldatoms
import numpy as np


class test_bendkickupdater(object):

    def setup(self):
        self.ensemble = coldatoms.Ensemble(num_ptcls=5)
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

        assert(np.linalg.norm(force.position[0] - expected_position) < 1.0e-8)

    def test_near_zero_field_ensemble_omegaB(self):
        Bz = 1.0e-30
        dt = 1.0

        self.ensemble.particle_properties['charge'] = np.ones(self.ensemble.v.shape[0])
        self.ensemble.particle_properties['mass'] = np.ones(self.ensemble.v.shape[0])
        self.ensemble.ensemble_properties = {}

        expected_position =  self.ensemble.x[0] + dt * self.ensemble.v[0]
        expected_velocity = self.ensemble.v[0]

        coldatoms.bend_kick(dt, Bz, self.ensemble, [])

        assert(np.linalg.norm(self.ensemble.x[0] - expected_position) < 1.0e-8)
        assert(np.linalg.norm(self.ensemble.v[0] - expected_velocity) < 1.0e-8)

    def test_closed_circle_ensemble_omegaB(self):
        Bz = 1.0
        q = self.ensemble.ensemble_properties['charge']
        m = self.ensemble.ensemble_properties['mass']
        omegaB = Bz * q / m
        dt = 2.0 * np.pi / omegaB

        self.ensemble.particle_properties['charge'] = q * np.ones(self.ensemble.v.shape[0])
        self.ensemble.particle_properties['mass'] = m * np.ones(self.ensemble.v.shape[0])
        self.ensemble.ensemble_properties = {}

        expected_position =  self.ensemble.x[0]
        expected_velocity = self.ensemble.v[0]

        coldatoms.bend_kick(dt, Bz, self.ensemble, [])

        assert(np.linalg.norm(self.ensemble.x[0] - expected_position) < 1.0e-8)
        assert(np.linalg.norm(self.ensemble.v[0] - expected_velocity) < 1.0e-8)

    def test_spot_check(self):
        Bz = 1.7
        q = self.ensemble.ensemble_properties['charge']
        m = self.ensemble.ensemble_properties['mass']
        dt = 1.2e-7

        initial_positions = np.random.random(self.ensemble.x.shape)
        initial_velocities = np.random.random(self.ensemble.v.shape)

        self.ensemble.x = np.copy(initial_positions)
        self.ensemble.v = np.copy(initial_velocities)

        coldatoms.bend_kick(dt, Bz, self.ensemble, [])
        final_positions = np.copy(self.ensemble.x)
        final_velocities = np.copy(self.ensemble.v)

        # now compute the reference solution
        self.ensemble.x = np.copy(initial_positions)
        self.ensemble.v = np.copy(initial_velocities)
        coldatoms.bend_kick(dt, Bz, self.ensemble, [], reference_impl=True)
        final_positions_ref = np.copy(self.ensemble.x)
        final_velocities_ref = np.copy(self.ensemble.v)

        assert(np.linalg.norm(final_positions - final_positions_ref) < 1.0e-6)
        assert(np.linalg.norm(final_velocities - final_velocities_ref) < 1.0e-6)
    def test_spot_check_per_particle(self):
        Bz = 1.7
        q = self.ensemble.ensemble_properties['charge']
        m = self.ensemble.ensemble_properties['mass']
        dt = 1.2e-7

        self.ensemble.particle_properties['charge'] = q * np.ones(self.ensemble.v.shape[0])
        self.ensemble.particle_properties['mass'] = m * np.ones(self.ensemble.v.shape[0])
        self.ensemble.ensemble_properties = {}

        initial_positions = np.random.random(self.ensemble.x.shape)
        initial_velocities = np.random.random(self.ensemble.v.shape)

        self.ensemble.x = np.copy(initial_positions)
        self.ensemble.v = np.copy(initial_velocities)

        coldatoms.bend_kick(dt, Bz, self.ensemble, [])
        final_positions = np.copy(self.ensemble.x)
        final_velocities = np.copy(self.ensemble.v)

        # now compute the reference solution
        self.ensemble.x = np.copy(initial_positions)
        self.ensemble.v = np.copy(initial_velocities)
        coldatoms.bend_kick(dt, Bz, self.ensemble, [], reference_impl=True)
        final_positions_ref = np.copy(self.ensemble.x)
        final_velocities_ref = np.copy(self.ensemble.v)

        assert(np.linalg.norm(final_positions - final_positions_ref) < 1.0e-6)
        assert(np.linalg.norm(final_velocities - final_velocities_ref) < 1.0e-6)
