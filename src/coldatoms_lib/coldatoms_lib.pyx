import cython
import numpy as np
cimport numpy as np


cdef extern from "forces.h":
    void coulomb_force(const double* positions, double charge,
                       int num_ptcls, double delta, double k, double* forces);
    void coulomb_force_per_particle_charges(const double* positions, double* charge,
                       int num_ptcls, double delta, double k, double* forces);


@cython.boundscheck(False)
@cython.wraparound(False)
def coulomb_force(
    np.ndarray[double, ndim=2, mode="c"] positions not None,
    double charge, double delta, double k,
    np.ndarray[double, ndim=2, mode="c"] forces not None):

    cdef num_ptcls
    num_ptcls = positions.shape[0]

    ccoldatoms_lib.coulomb_force(
        &positions[0, 0], charge, num_ptcls, delta, k, &forces[0, 0])
    

@cython.boundscheck(False)
@cython.wraparound(False)
def coulomb_force_per_particle_charge(
    np.ndarray[double, ndim=2, mode="c"] positions not None,
    np.ndarray[double, ndim=1, mode="c"] charges not None,
    double delta, double k,
    np.ndarray[double, ndim=2, mode="c"] forces not None):

    cdef num_ptcls
    num_ptcls = positions.shape[0]

    ccoldatoms_lib.coulomb_force_per_particle_charges(
        &positions[0, 0], &charges[0], num_ptcls, delta, k, &forces[0, 0])
