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
	int m;
	for (m = 0; m < NUM_COMPONENTS; ++m) {
		r[m] = r0[m] - r1[m];
	}
	double dist = distance(r, delta);
	double dist_cubed = dist * dist * dist;
	for (m = 0; m < NUM_COMPONENTS; ++m) {
		f[m] += kij * r[m] / dist_cubed;
	}
}

void ca_coulomb_force(const double *positions, double charge, double dt,
	int num_ptcls,
	double delta, double k, double *forces)
{
	double kij = charge * charge * dt * k;
	int i, j;
	for (i = 0; i < num_ptcls; ++i) {
		const double *r0 = &positions[i * NUM_COMPONENTS];
		double *f = &forces[i * NUM_COMPONENTS];
		for (j = 0; j < num_ptcls; ++j) {
			if (j == i) continue;
			const double *r1 = &positions[j * NUM_COMPONENTS];
			coulomb_force_one_pair(r0, r1, kij, delta, f);
		}
	}
}

void ca_coulomb_force_per_particle_charge(const double *positions,
					const double *charge, double dt, int num_ptcls,
					double delta, double k, double *forces)
{
	double kp = dt * k;
	int i, j;
	for (i = 0; i < num_ptcls; ++i) {
		double ki = kp * charge[i];
		const double *r0 = &positions[i * NUM_COMPONENTS];
		double *f = &forces[i * NUM_COMPONENTS];
		for (j = 0; j < num_ptcls; ++j) {
			if (j == i) continue;
			const double *r1 = &positions[j * NUM_COMPONENTS];
			double kij = ki * charge[j];
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

	int i;
	for (i = 0; i < num_ptcls; ++i) {
		double x = positions[i * NUM_COMPONENTS + 0];
		double y = positions[i * NUM_COMPONENTS + 1];
		double z = positions[i * NUM_COMPONENTS + 2];
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
	int i;

	for (i = 0; i < num_ptcls; ++i) {
		double alpha = q[i] * dt;
		double x = positions[i * NUM_COMPONENTS + 0];
		double y = positions[i * NUM_COMPONENTS + 1];
		double z = positions[i * NUM_COMPONENTS + 2];
		forces[i * NUM_COMPONENTS + 0] += alpha * (
			(-kx * SQR(cphi) - ky * SQR(sphi)) * x +
			cphi * sphi * (ky - kx) * y);
		forces[i * NUM_COMPONENTS + 1] += alpha * (
			cphi * sphi * (ky - kx) * x +
			(-kx * SQR(sphi) - ky * SQR(cphi)) * y);
		forces[i * NUM_COMPONENTS + 2] += -alpha * kz * z;
	}
}
