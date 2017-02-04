import numpy as np

class Ensemble(object):
    """An ensemble of particles.

    All ensembles have particle positions and velocities. In addition, an
    ensemble may define ensemble properties and per particle properties."""

    def __init__(self, num_ptcls=1):
        self.x = np.zeros([num_ptcls, 3], dtype=np.float64)
        self.v = np.zeros([num_ptcls, 3], dtype=np.float64)
        self.ensemble_properties = {}
        self.particle_properties = {}

    def get_num_ptcls(self):
        return self.x.shape[0]

    num_ptcls = property(get_num_ptcls,
                         'The number of particles in the ensemble')

    def set_particle_property(self, key, prop):
        """Set a particle property.

        key -- The name under which the property is stored.
        prop -- An array of the per particle properties. The array should have
        layout (num_ptcls, ...), i.e. the leading dimension should match the
        number of particles currently in the ensemble. We store a copy of
        prop."""

        if prop.shape[0] != self.num_ptcls:
            raise RuntimeError(
                'Size of property array does not match number of particles.')
        self.particle_properties[key] = np.copy(prop)


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

