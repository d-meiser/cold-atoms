#include <bend_kick_updater.h>
#include <math.h>


void bend_kick_update_scalar(double dt, double omegaB,
	int num_ptcls,
	double *restrict x, double *restrict v)
{
	double theta = dt * omegaB;
	double cosTheta = cos(theta);
	double sinTheta = sin(theta);

	double *x0 = &x[0 * num_ptcls];
	double *x1 = &x[1 * num_ptcls];
	double *x2 = &x[2 * num_ptcls];

	double *v0 = &v[0 * num_ptcls];
	double *v1 = &v[1 * num_ptcls];
	double *v2 = &v[2 * num_ptcls];

	for (int i = 0; i < num_ptcls; ++i) {
		x0[i] += (sinTheta          * v0[i] + (cosTheta - 1.0) * v1[i]) / omegaB;
		x1[i] += (-(cosTheta - 1.0) * v0[i] + sinTheta         * v1[i]) / omegaB;
		x2[i] += dt * v2[i];

		double vx_tmp = cosTheta * v0[i] - sinTheta * v1[i];
		double vy_tmp = sinTheta * v0[i] + cosTheta * v1[i];
		v0[i] = vx_tmp;
		v1[i] = vy_tmp;
	}
}

void bend_kick_update_vector(double dt, const double * restrict omegaB,
	int num_ptcls,
	double *restrict x, double * restrict v)
{
	double *x0 = &x[0 * num_ptcls];
	double *x1 = &x[1 * num_ptcls];
	double *x2 = &x[2 * num_ptcls];

	double *v0 = &v[0 * num_ptcls];
	double *v1 = &v[1 * num_ptcls];
	double *v2 = &v[2 * num_ptcls];

	for (int i = 0; i < num_ptcls; ++i) {
		double theta = dt * omegaB[i];
		double cosTheta = cos(theta);
		double sinTheta = sin(theta);

		x0[i] += (sinTheta * v0[i] + (cosTheta - 1.0) * v1[i]) / omegaB[i];
		x1[i] += (-(cosTheta - 1.0) * v0[i] + sinTheta * v0[i]) / omegaB[i];
		x2[i] += dt * v2[i];

		double vx_tmp = cosTheta * v0[i] - sinTheta * v1[i];
		double vy_tmp = sinTheta * v0[i] + cosTheta * v1[i];
		v0[i] = vx_tmp;
		v1[i] = vy_tmp;
	}
}

