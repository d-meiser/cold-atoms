import coldatoms
import numpy as np
import time


def measure_time(num_ptcls, per_ptcl_charges=False, num_iter=1, use_reference_impl=False):
    ensemble = coldatoms.Ensemble(num_ptcls=num_ptcls)
    ensemble.x = np.random.random([num_ptcls, 3])
    if per_ptcl_charges:
        ensemble.set_particle_properties('charge', np.random.random(num_ptcls))
    else:
        ensemble.ensemble_properties['charge'] = 1.0
    
    f = coldatoms.CoulombForce()
    if use_reference_impl:
        f.use_reference_implementations()
    
    accumulated_force = np.zeros_like(ensemble.v)
    
    t0 = time.time()
    for i in range(num_iter):
        f.force(1.0e-1, ensemble, accumulated_force)
    t1 = time.time()
    return t1 - t0


def num_ptcls(n_min, n_max, n):
    return n_min * (n_max / n_min)**(np.linspace(0.0, n - 1.0, n)/(n - 1))


nptcls = np.array(num_ptcls(1, 10000, 30))
times = np.array([measure_time(int(round(n)), num_iter=5) for n in nptcls])
pairs_per_second = nptcls**2 / times

print(nptcls)
print(pairs_per_second)

