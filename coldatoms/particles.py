import numpy as np


def push(dt, x, v, accelerations=[]):
    """Drift-Kick-Drift push of particles."""
    x += 0.5 * dt * v
    acc = np.zeros_like(v)
    for a in accelerations:
        acc += a(x, v)
    x += 0.5 * dt * v

