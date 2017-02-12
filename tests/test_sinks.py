from .context import coldatoms
import numpy as np


def test_create_sink_plane():
    sink = coldatoms.SinkPlane(
        np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))


def test_particle_hittling_plane_will_be_absorbed():
    sink = coldatoms.SinkPlane(
        np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))
    ensemble = coldatoms.Ensemble(num_ptcls=1)
    ensemble.x[0] = np.array([0.0, 0.0, -0.1])
    ensemble.v[0] = np.array([0.0, 0.0, 1.0])

    dt = 1.0
    times = sink.find_absorption_time(ensemble.x, ensemble.v, dt)
    assert(times[0] >= 0)
    assert(times[0] <= dt)


def test_moving_parallel_to_face_wont_be_absorbed():
    sink = coldatoms.SinkPlane(
        np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))
    ensemble = coldatoms.Ensemble(num_ptcls=1)
    ensemble.x[0] = np.array([0.0, 0.0, -0.1])
    ensemble.v[0] = np.array([0.0, 1.0e5, 0.0])

    dt = 1.0
    times = sink.find_absorption_time(ensemble.x, ensemble.v, dt)
    assert(times[0] < 0 or times[0] > dt)
