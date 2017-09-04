#ifndef RADIATION_PRESSURE_H
#define RADIATION_PRESSURE_H

struct CARandCtx;


/** Compute the number of scattered photons for resonance fluorescence

The number of scattered photons for saturated resonance fluorescence is
given by

nbar = dt S (gamma / (2pi)) (gamma/2)^2 / ((gamma/2)^2 (1 + 2 S) + delta^2)

where S is the laser field intensity in units of the saturation intensity,
gamma is the atomic linewidth, dt is the duration of the time interval,
and delta is the detuning from the atomic transition.
*/
void ca_compute_nbars(int n,
	double dt,
	double gamma,
	const double* s_of_r,
	const double* delta,
	double *nbar);

/*
Compute recoil momenta.  This function assumes an isotropic distribution of the
scattered photons.

n        is the number of atoms.
ctx      Random number generator context.
hbar_k   is the momentum of one photon.
nbar     is an array with the number of scattered photons for each atom.
recoils  contains the recoild momenta for each atom in format [px0 py0 pz0 px1
         py1 pz1 ...].
*/
void ca_add_radiation_pressure(int n,
        struct CARandCtx* ctx, 
	const double* hbar_k,
	const double* nbars,
	double* f);

#endif

