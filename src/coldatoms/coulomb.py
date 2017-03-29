import numpy as np

class CoulombForce(object):

    _epsilon0 = 8.854e-12
    _k = 4.0 * np.pi * _epsilon0

    def __init__(self):
        self.delta = 0.0

    def force(self, dt, ensemble):
        positions = ensemble.x
        f = np.zeros([ensemble.num_ptcls, 3])

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
            kp = self._k * q * q
            for i in range(ensemble.num_ptcls):
                for j in range(ensemble.num_ptcls):
                    r = positions[i] - positions[j]
                    absr = np.sqrt(r.dot(r) + my_delta_squared)
                    f[i] += kp * r / (absr * absr * absr)
        elif 'charge' in ensemble.particle_properties:
            q = ensemble.particle_properties['charge']
            for i in range(ensemble.num_ptcls):
                for j in range(ensemble.num_ptcls):
                    r = positions[i] - positions[j]
                    absr = np.sqrt(r.dot(r) + my_delta_squared)
                    f[i] += self._k * q[i] * q[j] * r / (absr * absr * absr)
        else:
            raise RuntimeError('Must provide a charge to compute coulomb force')

        return f

