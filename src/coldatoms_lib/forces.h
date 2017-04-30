#ifndef COLDATOMS_FORCES_H
#define COLDATOMS_FORCES_H

void coulomb_force (const double *positions, double charge, double dt,
		    int num_ptcls, double delta, double k, double *forces);

void coulomb_force_per_particle_charges (const double *positions,
					 const double *charge, double dt,
					 int num_ptcls, double delta, double k,
					 double *forces);

#endif
