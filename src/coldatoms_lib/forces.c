#include <forces.h>
#include <math.h>
#include <assert.h>
#include <stdio.h>


#define SQR(a) ((a) * (a))
#define NUM_COMPONENTS 3


static double distance(const double *r, double delta)
{
	double dist = 0.0;
	int i;
	for (i = 0; i < 3; ++i) {
		dist += r[i] * r[i];
	}
	dist += delta;
	return sqrt(dist);
}

static void coulomb_force_one_pair(const double *r0, const double *r1,
	double kij, double delta,  double *f)
{
	double r[NUM_COMPONENTS];
	double dist, dist_cubed;
	int m;
	for (m = 0; m < NUM_COMPONENTS; ++m) {
		r[m] = r0[m] - r1[m];
	}
	dist = distance(r, delta);
	dist_cubed = dist * dist * dist;
	for (m = 0; m < NUM_COMPONENTS; ++m) {
		f[m] += kij * r[m] / dist_cubed;
	}
}

void ca_coulomb_force(const double *positions, double charge, double dt,
	int num_ptcls,
	double delta, double k, double *forces)
{
	double kij = charge * charge * dt * k;
	const double *r0;
	double *f;
	const double *r1;
	int i, j;

	for (i = 0; i < num_ptcls; ++i) {
		r0 = &positions[i * NUM_COMPONENTS];
		f = &forces[i * NUM_COMPONENTS];
		for (j = 0; j < num_ptcls; ++j) {
			if (j == i) continue;
			r1 = &positions[j * NUM_COMPONENTS];
			coulomb_force_one_pair(r0, r1, kij, delta, f);
		}
	}
}

void ca_coulomb_force_per_particle_charge(const double *positions,
					const double *charge, double dt, int num_ptcls,
					double delta, double k, double *forces)
{
	double kp = dt * k;
	double ki;
	const double *r0;
	double *f;
	const double *r1;
	double kij;
	int i, j;

	for (i = 0; i < num_ptcls; ++i) {
		ki = kp * charge[i];
		r0 = &positions[i * NUM_COMPONENTS];
		f = &forces[i * NUM_COMPONENTS];
		for (j = 0; j < num_ptcls; ++j) {
			if (j == i) continue;
			r1 = &positions[j * NUM_COMPONENTS];
			kij = ki * charge[j];
			coulomb_force_one_pair(r0, r1, kij, delta, f);
		}
	}
}

void ca_harmonic_trap_forces(const double * positions,
	double q,
	double kx, double ky, double kz, double phi,
	double dt, int num_ptcls, double * forces)
{
	double cphi = cos(phi);
	double sphi = sin(phi);

	double alpha = q * dt;
	double x, y, z;

	int i;
	for (i = 0; i < num_ptcls; ++i) {
		x = positions[i * NUM_COMPONENTS + 0];
		y = positions[i * NUM_COMPONENTS + 1];
		z = positions[i * NUM_COMPONENTS + 2];
		forces[i * NUM_COMPONENTS + 0] += alpha * (
			(-kx * SQR(cphi) - ky * SQR(sphi)) * x +
			cphi * sphi * (ky - kx) * y);
		forces[i * NUM_COMPONENTS + 1] += alpha * (
			cphi * sphi * (ky - kx) * x +
			(-kx * SQR(sphi) - ky * SQR(cphi)) * y);
		forces[i * NUM_COMPONENTS + 2] += -alpha * kz * z;
	}
}

void ca_harmonic_trap_forces_per_particle_charge(
	const double * positions,
	const double * q,
	double kx, double ky, double kz, double phi,
	double dt, int num_ptcls,
	double * forces)
{
	double cphi = cos(phi);
	double sphi = sin(phi);
	double alpha, x, y, z;
	int i;

	for (i = 0; i < num_ptcls; ++i) {
		alpha = q[i] * dt;
		x = positions[i * NUM_COMPONENTS + 0];
		y = positions[i * NUM_COMPONENTS + 1];
		z = positions[i * NUM_COMPONENTS + 2];
		forces[i * NUM_COMPONENTS + 0] += alpha * (
			(-kx * SQR(cphi) - ky * SQR(sphi)) * x +
			cphi * sphi * (ky - kx) * y);
		forces[i * NUM_COMPONENTS + 1] += alpha * (
			cphi * sphi * (ky - kx) * x +
			(-kx * SQR(sphi) - ky * SQR(cphi)) * y);
		forces[i * NUM_COMPONENTS + 2] += -alpha * kz * z;
	}
}
