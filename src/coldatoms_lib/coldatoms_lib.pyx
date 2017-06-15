import cython
import numpy as np
cimport numpy as np
cimport ccoldatoms_lib


@cython.boundscheck(False)
@cython.wraparound(False)
def coulomb_force(
    np.ndarray[double, ndim=2, mode="c"] positions not None,
    double charge, double dt, double delta, double k,
    np.ndarray[double, ndim=2, mode="c"] forces not None):

    cdef num_ptcls
    num_ptcls = positions.shape[0]

    ccoldatoms_lib.coulomb_force(
        &positions[0, 0], charge, dt, num_ptcls, delta, k, &forces[0, 0])
    

@cython.boundscheck(False)
@cython.wraparound(False)
def coulomb_force_per_particle_charge(
    np.ndarray[double, ndim=2, mode="c"] positions not None,
    np.ndarray[double, ndim=1, mode="c"] charges not None,
    double dt, double delta, double k,
    np.ndarray[double, ndim=2, mode="c"] forces not None):

    cdef num_ptcls
    num_ptcls = positions.shape[0]

    ccoldatoms_lib.coulomb_force_per_particle_charges(
        &positions[0, 0], &charges[0], dt, num_ptcls, delta, k, &forces[0, 0])


@cython.boundscheck(False)
@cython.wraparound(False)
def bend_kick_update_scalar(
    double dt, double omegaB,
    np.ndarray[double, ndim=2, mode="c"] x not None,
    np.ndarray[double, ndim=2, mode="c"] v not None):

    cdef num_ptcls
    num_ptcls = x.shape[0]

    ccoldatoms_lib.bend_kick_update_scalar(
        dt, omegaB, num_ptcls, &x[0, 0], &v[0, 0])


@cython.boundscheck(False)
@cython.wraparound(False)
def bend_kick_update_vector(
    double dt,
    np.ndarray[double, ndim=1, mode="c"] omegaB,
    np.ndarray[double, ndim=2, mode="c"] x not None,
    np.ndarray[double, ndim=2, mode="c"] v not None):

    cdef num_ptcls
    num_ptcls = x.shape[0]

    ccoldatoms_lib.bend_kick_update_vector(
        dt, &omegaB[0], num_ptcls, &x[0, 0], &v[0, 0])


def bend_kick_update(dt, omegaB, x, v):
    if np.isscalar(omegaB):
        bend_kick_update_scalar(dt, omegaB, x, v)
    else:
        bend_kick_update_vector(dt, omegaB, x, v)


class Rng(object):

    def fill(self, array):
        array.fill(0.5)

