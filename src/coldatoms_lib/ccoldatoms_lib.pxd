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

cdef extern from "ca_rand.h":
    struct CARandCtx:
        pass
    CARandCtx* ca_rand_create();
    void ca_rand_destroy(CARandCtx** ctx);
    void ca_rand_seed(CARandCtx* ctx, int seed);
    void ca_rand(CARandCtx* ctx, int n, double* x);
    void ca_rand_gaussian(CARandCtx* ctx, int n, double mean, double std, double* x);
    void ca_rand_poisson(CARandCtx* ctx, int n, double nbar, int* x);

