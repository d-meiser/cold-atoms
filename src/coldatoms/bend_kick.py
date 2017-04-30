import numpy as np


def bend_kick_update(dt, omegaB, x, v):
    theta = dt * omegaB
    cosTheta = np.cos(theta)
    sinTheta = np.sin(theta)

    x[:, 0] = x[:, 0] + (
        sinTheta * v[:, 0] + (cosTheta - 1.0) * v[:, 1]) / omegaB
    x[:, 1] = x[:, 1] + (
        -(cosTheta - 1.0) * v[:, 0] + sinTheta * v[:, 1]) / omegaB

    vx = cosTheta * v[:, 0] - sinTheta * v[:, 1]
    v[:, 1] = sinTheta * v[:, 0] + cosTheta * v[:, 1]
    v[:, 0] = vx


def bend_kick(dt, Bz, ensemble, forces):
    """Integrator for particle motion in a constant magnetic field"""

    if 'charge' in ensemble.ensemble_properties:
        q = ensemble.ensemble_properties['charge']
    elif 'charge' in ensemble.particle_properties:
        q = ensemble.particle_properties['charge']
    else:
        raise RuntimeError('Must provide a charge for bend_kick update.')

    if 'mass' in ensemble.ensemble_properties:
        m = ensemble.ensemble_properties['mass']
    elif 'mass' in ensemble.particle_properties:
        m = ensemble.particle_properties['mass']
    else:
        raise RuntimeError('Must provide a mass for bend_kick update.')

    omegaB = Bz * q / m

    if len(forces) == 0:
        bend_kick_update(dt, omegaB, ensemble.x, ensemble.v)
    else:
        bend_kick_update(0.5 * dt, omegaB, ensemble.x, ensemble.v)
        f = np.zeros_like(ensemble.v)
        for force in forces:
            force.force(dt, ensemble, f)
        ensemble.v *= f / m
        bend_kick_update(0.5 * dt, omegaB, ensemble.x, ensemble.v)
