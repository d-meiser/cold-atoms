#ifndef COLDATOMS_FORCES_H
#define COLDATOMS_FORCES_H

void coulomb_force(const double* positions, double charge,
                   int num_ptcls, double delta, double* forces);

#endif
