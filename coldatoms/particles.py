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

    def resize(self, new_size):
        shape = [self.x.shape]
        shape[0] = new_size
        self.x.resize(shape)
        self.v.resize(shape)
        for particle_prop in self.particle_properties:
            shape = [self.particle_properties[particle_prop].shape]
            shape[0] = new_size
            self.particle_properties[particle_prop].resize(shape)



class Source(object):
    """A particle source."""

    def __init__(self):
        pass

    def num_ptcls_produced(self):
        return 0

    def produce_ptcls(start, end, ensemble):
        pass


def produce_particles(ensemble, sources=[]):
    """Insert particles produced by sources into the ensemble.

    ensemble -- The ensemble into which to insert the particles.
    sources -- The particle source. Should derive from Source.
    """

    num_new_ptcls = []
    tot_new_ptcls = 0
    for s in sources:
        num_new_ptcls.append(s.num_ptcls_produced())
        tot_new_ptcls += num_new_ptcls[-1]

    ensemble.resize(ensemble.num_ptcls + tot_new_ptcls)


def drift_kick(dt, ensemble, forces=[]):
    """Drift-Kick-Drift push of particles."""
    if len(forces) == 0:
        ensemble.x += dt * ensemble.v
    else:
        ensemble.x += 0.5 * dt * ensemble.v

        f = np.zeros_like(ensemble.v)
        for force in forces:
            f += force(ensemble)

        m = 0.0
        if 'mass' in ensemble.ensemble_properties:
            m = ensemble.ensemble_properties['mass']
        elif 'mass' in ensemble.particle_properties:
            m = ensemble.particle_properties['mass']
        else:
            raise RuntimeError('To accelerate particles we need a mass ensemble or particle property')
        ensemble.v += (dt / m) * f
        ensemble.x += 0.5 * dt * ensemble.v

