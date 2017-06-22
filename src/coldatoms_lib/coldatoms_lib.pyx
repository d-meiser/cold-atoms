import cython
import numpy as np
cimport numpy as np
cimport ccoldatoms_lib
import atexit
from libc.stdint cimport uintptr_t


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


cdef class Rng(object):

    cdef ccoldatoms_lib.CARandCtx* _generator

    def context(self):
        return <uintptr_t>self._generator

    def __cinit__(self, seed=None):
        self._generator = ccoldatoms_lib.ca_rand_create()
        if seed is not None:
            ccoldatoms_lib.ca_rand_seed(self._generator, seed)

    def __dealloc__(self):
        ccoldatoms_lib.ca_rand_destroy(&self._generator)

    def seed(self, unsigned int seed):
        ccoldatoms_lib.ca_rand_seed(self._generator, seed)

    def fill(self, np.ndarray[double, mode="c"] array):
        cdef int n = array.size
        cdef double *a = <double *>array.data
        ccoldatoms_lib.ca_rand(self._generator, n, a)

    def fill_gaussian(self, double mean, double std, np.ndarray[double, mode="c"] array):
        cdef int n = array.size
        cdef double *a = <double *>array.data
        ccoldatoms_lib.ca_rand_gaussian(self._generator, n, mean, std, a)

    def fill_poisson(self, double nbar, np.ndarray[int, mode="c"] array):
        cdef int n = array.size
        cdef int *a = <int *>array.data
        ccoldatoms_lib.ca_rand_poisson(self._generator, n, nbar, a)

    def fill_poisson_many(self, np.ndarray[double, mode="c"] nbars, np.ndarray[int, mode="c"] array):
        assert(nbars.size == array.size)
        cdef int n = array.size
        cdef double *ns = <double *>nbars.data
        cdef int *a = <int *>array.data
        ccoldatoms_lib.ca_rand_poisson_many(self._generator, n, ns, a)


"""For convenience we provide a random number generator."""
rng = Rng()


@cython.boundscheck(False)
@cython.wraparound(False)
def compute_nbars(double dt, double gamma, 
    np.ndarray[double, ndim=1, mode="c"] s_of_r not None,
    np.ndarray[double, ndim=1, mode="c"] delta not None,
    np.ndarray[double, ndim=1, mode="c"] nbar not None):
    assert(s_of_r.shape[0] == nbar.shape[0])
    assert(delta.shape[0] == nbar.shape[0])

    cdef num_ptcls
    num_ptcls = nbar.shape[0]

    ccoldatoms_lib.compute_nbars(num_ptcls, dt, gamma, &s_of_r[0], &delta[0], &nbar[0])

def compute_recoils(double hbar_k,
    uintptr_t rng_context,
    np.ndarray[int, ndim=1, mode="c"] ns not None,
    np.ndarray[double, ndim=2, mode="c"] recoils not None):
    assert(ns.size == recoils.shape[0])
    assert(recoils.shape[1] == 3)

    cdef num_ptcls
    num_ptcls = ns.shape[0]
    ccoldatoms_lib.compute_recoils(num_ptcls, <ccoldatoms_lib.CARandCtx*>rng_context, hbar_k, &ns[0], &recoils[0, 0])

