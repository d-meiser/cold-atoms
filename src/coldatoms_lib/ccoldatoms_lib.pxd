cdef extern from "forces.h":
    void coulomb_force(const double* positions, double charge,
                       int num_ptcls, double delta, double k, double* forces);
    void coulomb_force_per_particle_charges(const double* positions, double* charge,
                       int num_ptcls, double delta, double k, double* forces);
