#include <bend_kick_updater.h>
#include <math.h>

struct Vec3 {
	double x;
	double y;
	double z;
};

void ca_bend_kick_update_scalar(double dt, double omegaB,
	int num_ptcls,
	double * x, double * v)
{
	double theta = dt * omegaB;
	double cosTheta = cos(theta);
	double sinTheta = sin(theta);

	struct Vec3 *pos = (struct Vec3 *)x;
	struct Vec3 *vel = (struct Vec3 *)v;

	double m_pos[2][2] = {
		{sinTheta / omegaB, (cosTheta - 1.0) / omegaB},
		{-(cosTheta - 1.0) / omegaB, sinTheta / omegaB}};
	double m_vel[2][2] = {
		{cosTheta, -sinTheta},
		{sinTheta, cosTheta}};
	
	double vx_tmp;
	double vy_tmp;

	int i;

	for (i = 0; i < num_ptcls; ++i) {
		pos[i].x += m_pos[0][0] * vel[i].x + m_pos[0][1] * vel[i].y;
		pos[i].y += m_pos[1][0] * vel[i].x + m_pos[1][1] * vel[i].y;
		pos[i].z += dt * vel[i].z;

		vx_tmp = m_vel[0][0] * vel[i].x + m_vel[0][1] * vel[i].y;
		vy_tmp = m_vel[1][0] * vel[i].x + m_vel[1][1] * vel[i].y;

		vel[i].x = vx_tmp;
		vel[i].y = vy_tmp;
	}
}

void ca_bend_kick_update_vector(double dt, const double *  omegaB,
	int num_ptcls,
	double * x, double *  v)
{
	double theta, cosTheta, sinTheta, vx_tmp, vy_tmp;
	struct Vec3 *pos = (struct Vec3 *)x;
	struct Vec3 *vel = (struct Vec3 *)v;
	int i;

	for (i = 0; i < num_ptcls; ++i) {
		theta = dt * omegaB[i];
		cosTheta = cos(theta);
		sinTheta = sin(theta);

		pos[i].x += (sinTheta * vel[i].x + (cosTheta - 1.0) * vel[i].y) / omegaB[i];
		pos[i].y += (-(cosTheta - 1.0) * vel[i].x + sinTheta * vel[i].y) / omegaB[i];
		pos[i].z += dt * vel[i].z;

		vx_tmp = cosTheta * vel[i].x - sinTheta * vel[i].y;
		vy_tmp = sinTheta * vel[i].x + cosTheta * vel[i].y;
		vel[i].x = vx_tmp;
		vel[i].y = vy_tmp;
	}
}

