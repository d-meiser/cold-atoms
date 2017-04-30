cdef extern from "forces.h":
    void coulomb_force(const double* positions, double charge, double dt,
                       int num_ptcls, double delta, double k, double* forces);
    void coulomb_force_per_particle_charges(const double* positions,
                       double* charge, double dt, int num_ptcls, double delta,
                       double k, double* forces);

cdef extern from "bend_kick_updater.h":
    void bend_kick_update_scalar(double dt, double omegaB,
        int num_ptcls,
        double *x, double *v);
    
    void bend_kick_update_vector(double dt, const double *omegaB,
        int num_ptcls,
        double *x, double *v);
