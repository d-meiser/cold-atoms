import numpy as np
import coldatoms_lib


def bend_kick_update_reference_impl(dt, omegaB, x, v):
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


def bend_kick(dt, Bz, ensemble, forces, num_steps=1, reference_impl=False):
    """Integrator for particle motion in a constant magnetic field"""

    if num_steps < 1:
        return

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

    if reference_impl:
         updater = bend_kick_update_reference_impl
    else:
         updater = coldatoms_lib.bend_kick_update

    if len(forces) == 0:
        updater(num_steps * dt, omegaB, ensemble.x, ensemble.v)
    else:
        updater(0.5 * dt, omegaB, ensemble.x, ensemble.v)

        f = np.zeros_like(ensemble.v)

        for i in range(num_steps - 1):
            for force in forces:
                force.force(dt, ensemble, f)
            ensemble.v += f / m
            updater(dt, omegaB, ensemble.x, ensemble.v)
            f.fill(0.0)

        for force in forces:
            force.force(dt, ensemble, f)
        ensemble.v += f / m
        updater(0.5 * dt, omegaB, ensemble.x, ensemble.v)
