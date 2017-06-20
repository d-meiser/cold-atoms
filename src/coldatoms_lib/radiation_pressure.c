#include <radiation_pressure.h>

static const double two_pi = 2.0*3.14159265358979323846;
#define SQR(a) ((a) * (a))


static double scattering_rate(double gamma, double s, double delta);


void compute_nbars(int n,
	double dt,
	double gamma,
	const double* s_of_r,
	const double* delta,
	double *nbar)
{
	for (int i = 0; i < n; ++i) {
		nbar[i] = dt * scattering_rate(gamma, s_of_r[i], delta[i]);
	}
}

double scattering_rate(double gamma, double s, double delta)
{
	double nu = gamma / two_pi;
	double half_gamma_squared = 0.25 * gamma * gamma;
	return s * nu * half_gamma_squared /
		(half_gamma_squared * (1.0 + 2.0 * s) + SQR(delta));
}
