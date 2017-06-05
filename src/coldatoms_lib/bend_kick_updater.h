#ifndef BEND_KICK_UPDATER_H
#define BEND_KICK_UPDATER_H

void bend_kick_update_scalar(double dt, double omegaB,
	int num_ptcls, double *restrict x, double * restrict v);

void bend_kick_update_vector(double dt, const double * restrict omegaB,
	int num_ptcls, double *restrict x, double * restrict v);

#endif
