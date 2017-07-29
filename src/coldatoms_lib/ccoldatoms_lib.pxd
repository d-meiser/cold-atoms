cdef extern from "forces.h":
    void ca_coulomb_force(const double* positions, double charge, double dt,
                       int num_ptcls, double delta, double k, double* forces);
    void ca_coulomb_force_per_particle_charge(const double* positions,
                       double* charge, double dt, int num_ptcls, double delta,
                       double k, double* forces);
    void ca_harmonic_trap_forces(const double* positions, double q,
                       double kx, double ky, double kz, double phi, double dt,
                       int num_ptcls, double *forces);
    void ca_harmonic_trap_forces_per_particle_charge(const double* positions, const double* q,
                       double kx, double ky, double kz, double phi, double dt,
                       int num_ptcls, double *forces);


cdef extern from "bend_kick_updater.h":
    void ca_bend_kick_update_scalar(double dt, double omegaB,
        int num_ptcls,
        double *x, double *v);
    
    void ca_bend_kick_update_vector(double dt, const double *omegaB,
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
    void ca_rand_poisson_many(CARandCtx* ctx, int n, double* nbars, int* x);


cdef extern from "radiation_pressure.h":
    void ca_compute_nbars(int n, double dt, double gamma, const double* s_of_r,
        const double* delta, double* nbar);
    void ca_add_radiation_pressure(int n, CARandCtx* ctx, const double* hbar_k, const double* nbar, double* force);
