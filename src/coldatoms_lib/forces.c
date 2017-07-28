#include <forces.h>
#include <math.h>
#include <assert.h>
#include <stdio.h>
#include <float.h>

#define SQR(a) ((a) * (a))
#define DIST_CUBED_EPSILON (1.0e1 * DBL_MIN)
#define NUM_COMPONENTS 3


static double distance(const double *r, double delta)
{
	double dist = 0.0;
	for (int i = 0; i < 3; ++i) {
		dist += r[i] * r[i];
	}
	dist += delta;
	return sqrt(dist);
}

void coulomb_force(const double *positions, double charge, double dt,
	int num_ptcls,
	double delta, double k, double *forces)
{
	double kij = charge * charge * dt * k;
	const double *r0 = positions;
	for (int i = 0; i < num_ptcls; ++i) {
		const double *r1 = positions;
		for (int j = 0; j < num_ptcls; ++j) {
			if (j == i) {
				r1 += NUM_COMPONENTS;
				continue;
			}
			double r[NUM_COMPONENTS];
			for (int m = 0; m < NUM_COMPONENTS; ++m) {
				r[m] = r0[m] - r1[m];
			}
			double dist = distance(r, delta);
			double dist_cubed = dist * dist * dist;
			for (int m = 0; m < NUM_COMPONENTS; ++m) {
				forces[m] += kij * r[m] / dist_cubed;
			}
			r1 += NUM_COMPONENTS;
		}
		r0 += NUM_COMPONENTS;
		forces += NUM_COMPONENTS;
	}
}

void coulomb_force_per_particle_charge(const double *positions,
					const double *charge, double dt, int num_ptcls,
					double delta, double k, double *forces)
{
	double kp = dt * k;
	const double *r0 = positions;
	for (int i = 0; i < num_ptcls; ++i) {
		double ki = kp * charge[i];
		const double *r1 = positions;
		for (int j = 0; j < num_ptcls; ++j) {
			if (j == i) {
				r1 += NUM_COMPONENTS;
				continue;
			}
			double r[NUM_COMPONENTS];
			for (int m = 0; m < NUM_COMPONENTS; ++m) {
				r[m] = r0[m] - r1[m];
			}
			double dist = distance(r, delta);
			double dist_cubed = dist * dist * dist;
			double kij = ki * charge[j];
			for (int m = 0; m < NUM_COMPONENTS; ++m) {
				forces[m] += kij * r[m] / dist_cubed;
			}
			r1 += NUM_COMPONENTS;
		}
		r0 += NUM_COMPONENTS;
		forces += NUM_COMPONENTS;
	}
}

void harmonic_trap_forces(const double *restrict positions,
	double q,
	double kx, double ky, double kz, double phi,
	double dt, int num_ptcls, double *restrict forces)
{
	double cphi = cos(phi);
	double sphi = sin(phi);

	double alpha = q * dt;

	for (int i = 0; i < num_ptcls; ++i) {
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

void harmonic_trap_forces_per_particle_charge(
	const double *restrict positions,
	const double *restrict q,
	double kx, double ky, double kz, double phi,
	double dt, int num_ptcls,
	double *restrict forces)
{
	double cphi = cos(phi);
	double sphi = sin(phi);


	for (int i = 0; i < num_ptcls; ++i) {
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
