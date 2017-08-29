#ifndef BEND_KICK_UPDATER_H
#define BEND_KICK_UPDATER_H

#include <ca_utilities.h>


void ca_bend_kick_update_scalar(double dt, double omegaB,
	int num_ptcls, double *CA_RESTRICT x, double *CA_RESTRICT v);

void ca_bend_kick_update_vector(double dt, const double * CA_RESTRICT omegaB,
	int num_ptcls, double *CA_RESTRICT x, double *CA_RESTRICT v);

#endif
