from .context import coldatoms
import numpy as np


class SinkPlane(coldatoms.Sink):

    def __init__(self, point, normal):
        """Generate a sink that absorbs particles hitting a plane.

        point -- A point in the plane.
        normal -- A normal to the plane.
        """
        self.point = point
        self.normal = normal

    def find_absorption_time(self, x, v, dt):
        taus = np.zeros(x.shape[0])

        for i in range(x.shape[0]):
            normal_velocity = self.normal.dot(v[i])
            if (normal_velocity == 0.0):
                taus[i] = 2.0 * dt
            else:
                taus[i] = self.normal.dot(self.point - x[i]) / normal_velocity

        return taus



def test_create_sink_plane():
    sink = SinkPlane(np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))


def test_particle_hittling_plane_will_be_absorbed():
    sink = SinkPlane(np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))
    ensemble = coldatoms.Ensemble(num_ptcls=1)
    ensemble.x[0] = np.array([0.0, 0.0, -0.1])
    ensemble.v[0] = np.array([0.0, 0.0, 1.0])

    dt = 1.0
    times = sink.find_absorption_time(ensemble.x, ensemble.v, dt)
    assert(times[0] >= 0)
    assert(times[0] <= dt)

