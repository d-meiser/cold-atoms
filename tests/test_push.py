from .context import coldatoms
import numpy as np
import math


def test_zero_velocities():
    x = np.random.rand(3)
    v = np.zeros(3)
    x_old = x.copy()
    coldatoms.drift_kick(1.0, 0.1, x, v)
    assert(x == x_old).all()


def test_zero_accelerations():
    x = np.random.rand(3)
    v = np.random.rand(3)
    v_old = v.copy()
    coldatoms.drift_kick(1.0, 1.0, x, v)
    assert(v == v_old).all()


class Harmonic():
    def __init__(self, k):
        self.k = k

    def __call__(self, x, v):
        # TODO: There has to be a better way to construct this
        # array.
        accelerations = np.transpose(np.array(
            [-self.k[i] * x[:, i] for i in range(3)]))
        return accelerations


def test_harmonic_potential_motion_is_bounded():
    x = np.random.rand(5, 3)
    v = np.random.rand(5, 3)
    initial_stddev_vel = np.linalg.norm(v)

    harmonic = Harmonic([1.0, 2.0, 3.0])
    for i in range(100):
        coldatoms.drift_kick(1.0, 1.0, x, v, [harmonic])

    stddev_vel = np.linalg.norm(v)
    assert(stddev_vel < 10.0 * initial_stddev_vel)


def test_harmonic_spot():
    x = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    v = np.zeros_like(x)

    t = 0
    dt = 0.02
    m = 4.0
    k = [1.0, 2.0, 3.0]
    harmonic = Harmonic(k)

    for i in range(50):
        coldatoms.drift_kick(dt, m, x, v, [harmonic])
        t += dt

    omega_x = math.sqrt(k[0] / m)
    assert(abs(x[0, 0] - math.cos(t * omega_x)) < dt*dt)

    omega_y = math.sqrt(k[1] / m)
    assert(abs(x[1, 1] - math.cos(t * omega_y)) < dt*dt)

    omega_z = math.sqrt(k[2] / m)
    assert(abs(x[2, 2] - math.cos(t * omega_z)) < dt*dt)


if __name__ == '__main__':
    unittest.main()

