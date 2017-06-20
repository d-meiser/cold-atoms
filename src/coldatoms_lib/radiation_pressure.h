#ifndef RADIATION_PRESSURE_H
#define RADIATION_PRESSURE_H

/** Compute the number of scattered photons for resonance fluorescence

The number of scattered photons for saturated resonance fluorescence is
given by

nbar = dt S (gamma / (2pi)) (gamma/2)^2 / ((gamma/2)^2 (1 + 2 S) + delta^2)

where S is the laser field intensity in units of the saturation intensity,
gamma is the atomic linewidth, dt is the duration of the time interval,
and delta is the detuning from the atomic transition.
*/
void compute_nbars(int n,
	double dt,
	double gamma,
	const double* s_of_r,
	const double* delta,
	double *nbar);

#endif

