#ifndef BEND_KICK_UPDATER_H
#define BEND_KICK_UPDATER_H


void ca_bend_kick_update_scalar(double dt, double omegaB,
	int num_ptcls, double *x, double *v);

void ca_bend_kick_update_vector(double dt, const double *  omegaB,
	int num_ptcls, double *x, double *v);

#endif
