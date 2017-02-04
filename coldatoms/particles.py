import numpy as np


def drift_kick(dt, m, x, v, forces=[]):
    """Drift-Kick-Drift push of particles."""
    if len(forces) == 0:
        x += dt * v
    else:
        x += 0.5 * dt * v
        f = np.zeros_like(v)
        for force in forces:
            f += force(x, v)
        v += (dt / m) * f
        x += 0.5 * dt * v

