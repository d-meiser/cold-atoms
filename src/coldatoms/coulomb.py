import numpy as np

class CoulombForce(object):

    _epsilon0 = 8.854e-12
    _k = 4.0 * np.pi * _epsilon0

    def force(self, dt, ensemble):
        positions = ensemble.x
        f = np.zeros([ensemble.num_ptcls, 3])

        if 'charge' in ensemble.ensemble_properties:
            q = ensemble.ensemble_properties['charge']
            kp = self._k * q * q
            for i in range(ensemble.num_ptcls):
                for j in range(ensemble.num_ptcls):
                    if i != j:
                        r = positions[i] - positions[j]
                        absr = np.linalg.norm(r)
                        f[i] += kp * r / (absr * absr * absr)

        elif 'charge' in ensemble.particle_properties:
            q = ensemble.particle_properties['charge']
            for i in range(ensemble.num_ptcls):
                for j in range(ensemble.num_ptcls):
                    if i != j:
                        r = positions[i] - positions[j]
                        absr = np.linalg.norm(r)
                        f[i] += self._k * q[i] * q[j] * r / (absr * absr * absr)
        else:
            raise RuntimeError('Must provide a charge to compute coulomb force')

        return f

