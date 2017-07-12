#ifndef COLDATOMS_FORCES_H
#define COLDATOMS_FORCES_H

void coulomb_force (const double *positions, double charge, double dt,
		    int num_ptcls, double delta, double k, double *forces);

void coulomb_force_per_particle_charges (const double *positions,
					 const double *charge, double dt,
					 int num_ptcls, double delta, double k,
					 double *forces);

void harmonic_trap_forces(const double *positions, double q,
	double kx, double ky, double kz, double phi,
	double dt, int num_ptcls, double *forces);

void harmonic_trap_forces_per_particle_charges(
        const double *positions, const double *q,
	double kx, double ky, double kz, double phi,
	double dt, int num_ptcls, double *forces);

#endif
