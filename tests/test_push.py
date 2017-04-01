import coldatoms
import numpy as np
import math
from nose.tools import *


def test_zero_velocities():
    ensemble = coldatoms.Ensemble(num_ptcls=3)
    ensemble.x = np.random.rand(3)
    ensemble.v = np.zeros(3)
    x_old = ensemble.x.copy()
    coldatoms.drift_kick(1.0, ensemble)
    assert(ensemble.x == x_old).all()


def test_zero_accelerations():
    ensemble = coldatoms.Ensemble(num_ptcls=3)
    ensemble.x = np.random.rand(3)
    ensemble.v = np.zeros(3)
    v_old = ensemble.v.copy()
    coldatoms.drift_kick(1.0, ensemble)
    assert(ensemble.v == v_old).all()


class Harmonic():
    def __init__(self, k):
        self.k = k

    def force(self, dt, ensemble):
        # TODO: There has to be a better way to construct this
        # array.
        accelerations = dt * np.transpose(np.array(
            [-self.k[i] * ensemble.x[:, i] for i in range(3)]))
        return accelerations


def test_harmonic_potential_motion_is_bounded():
    ensemble = coldatoms.Ensemble(num_ptcls=5)
    ensemble.x = np.random.rand(5, 3)
    ensemble.v = np.random.rand(5, 3)
    initial_stddev_vel = np.linalg.norm(ensemble.v)

    m = 3.4
    ensemble.ensemble_properties['mass'] = m

    harmonic = Harmonic([1.0, 2.0, 3.0])
    for i in range(100):
        coldatoms.drift_kick(1.0, ensemble, [harmonic])

    stddev_vel = np.linalg.norm(ensemble.v)
    assert(stddev_vel < 10.0 * initial_stddev_vel)


def test_harmonic_spot():
    ensemble = coldatoms.Ensemble(num_ptcls=3)
    ensemble.x = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    ensemble.v = np.zeros_like(ensemble.x)

    t = 0
    dt = 0.02
    m = 4.0
    ensemble.ensemble_properties['mass'] = m
    k = [1.0, 2.0, 3.0]
    harmonic = Harmonic(k)

    for i in range(50):
        coldatoms.drift_kick(dt, ensemble, [harmonic])
        t += dt

    omega_x = math.sqrt(k[0] / m)
    assert(abs(ensemble.x[0, 0] - math.cos(t * omega_x)) < dt*dt)

    omega_y = math.sqrt(k[1] / m)
    assert(abs(ensemble.x[1, 1] - math.cos(t * omega_y)) < dt*dt)

    omega_z = math.sqrt(k[2] / m)
    assert(abs(ensemble.x[2, 2] - math.cos(t * omega_z)) < dt*dt)


def test_can_use_per_particle_masses():
    ensemble = coldatoms.Ensemble(num_ptcls=3)
    ensemble.x = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    ensemble.v = np.zeros_like(ensemble.x)
    ensemble.set_particle_property('mass', np.ones(3)) 

    dt = 0.02
    k = [1.0, 2.0, 3.0]
    harmonic = Harmonic(k)

    coldatoms.drift_kick(dt, ensemble, [harmonic])


@raises(Exception)
def test_have_to_provide_mass():
    ensemble = coldatoms.Ensemble(num_ptcls=3)
    ensemble.x = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    ensemble.v = np.zeros_like(ensemble.x)

    k = [1.0, 2.0, 3.0]
    harmonic = Harmonic(k)

    coldatoms.drift_kick(0.1, ensemble, [harmonic])


if __name__ == '__main__':
    unittest.main()

