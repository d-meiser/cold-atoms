import numpy as np
import coldatoms_lib


def _coulomb_force_ref(positions, q, dt, delta, k, f):
    kp = dt * k * q * q
    num_ptcls = positions.shape[0]
    for i in range(num_ptcls):
        for j in range(num_ptcls):
            r = positions[i] - positions[j]
            absr = np.sqrt(r.dot(r) + delta)
            f[i] += kp * r / (absr * absr * absr)


def _coulomb_force_ref_per_particle_charges(positions, q, dt,
                                            delta, k, f):
    num_ptcls = positions.shape[0]
    k *= dt
    for i in range(num_ptcls):
        for j in range(num_ptcls):
            r = positions[i] - positions[j]
            absr = np.sqrt(r.dot(r) + delta)
            f[i] += k * q[i] * q[j] * r / (absr * absr * absr)


class CoulombForce(object):

    _epsilon0 = 8.854187817620e-12
    _k = 1.0 / (4.0 * np.pi * _epsilon0)

    def __init__(self):
        self.delta = 0.0
        self.coulomb_force = coldatoms_lib.coulomb_force
        self.coulomb_force_per_particle_charges = coldatoms_lib.coulomb_force_per_particle_charge

    def use_reference_implementations(self):
        self.coulomb_force = _coulomb_force_ref
        self.coulomb_force_per_particle_charges = _coulomb_force_ref_per_particle_charges

    def force(self, dt, ensemble, f):
        positions = ensemble.x

        # We guard against the case where particles are in the same
        # location by adding a small cut off parameter to the
        # softcore parameter. This cut off parameter is designed so that
        # the distance raised to the third power is still different
        # from zero so we can savely divide.
        ulp = np.finfo(ensemble.x.dtype).tiny
        my_delta_squared = (self.delta * self.delta +
                            1.0e1 * ulp **(2.0/3.0))

        if 'charge' in ensemble.ensemble_properties:
            q = ensemble.ensemble_properties['charge']
            self.coulomb_force(positions, q, dt,
                               my_delta_squared, self._k, f)
        elif 'charge' in ensemble.particle_properties:
            q = ensemble.particle_properties['charge']
            self.coulomb_force_per_particle_charges(
                positions, q, dt, my_delta_squared, self._k, f)
        else:
            raise RuntimeError('Must provide a charge to compute coulomb force')

