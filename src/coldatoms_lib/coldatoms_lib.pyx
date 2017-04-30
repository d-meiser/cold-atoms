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

