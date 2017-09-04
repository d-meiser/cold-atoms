#include <radiation_pressure.h>
#include <ca_rand.h>
#include <math.h>
#include <assert.h>

static const double two_pi = 2.0*3.14159265358979323846;
#define SQR(a) ((a) * (a))


static double scattering_rate(double gamma, double s, double delta);


void ca_compute_nbars(int n,
	double dt,
	double gamma,
	const double* s_of_r,
	const double* delta,
	double *nbar)
{
	int i;
	for (i = 0; i < n; ++i) {
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

static void add_radiation_pressure_large_n(
	struct CARandCtx* ctx,
	const double* hbar_k,
	double hbar_k_nrm,
	int n,
	double* f)
{
	double recoil[3];
	int i;

	ca_rand_gaussian(ctx, 3, 0.0, hbar_k_nrm * sqrt(n / 3.0), recoil);
	for (i = 0; i < 3; ++i) {
		f[i] += n * hbar_k[i] + recoil[i];
	}
}

#define CA_LARGE_N 128

/*
For small numbers of scattered photons we add up the recoil due to n discrete
photons scattered into random directions (isotropically).
*/
static void add_radiation_pressure_small_n(
	struct CARandCtx* ctx,
	const double* hbar_k,
	double hbar_k_nrm,
	int n,
	double* f)
{
	double directions[3][CA_LARGE_N];
	double nrms[CA_LARGE_N] = { 0.0 };
	double recoil[3] = { 0.0 };
	int i, j;

	if (0 == n) return;
	assert(n <= CA_LARGE_N);

	ca_rand_gaussian(ctx, n, 0.0, 1.0, &directions[0][0]);
	ca_rand_gaussian(ctx, n, 0.0, 1.0, &directions[1][0]);
	ca_rand_gaussian(ctx, n, 0.0, 1.0, &directions[2][0]);

	for (i = 0; i < 3; ++i) {
		for (j = 0; j < n; ++j) {
			nrms[j] += SQR(directions[i][j]);
		}
	}
	for (j = 0; j < n; ++j) {
		nrms[j] = sqrt(nrms[j]);
	}
	for (i = 0; i < 3; ++i) {
		for (j = 0; j < n; ++j) {
			directions[i][j] /= nrms[j];
		}
	}

	for (i = 0; i < 3; ++i) {
		for (j = 0; j < n; ++j) {
			recoil[i] += directions[i][j];
		}
		recoil[i] *= hbar_k_nrm;
	}
	for (i = 0; i < 3; ++i) {
		f[i] += n * hbar_k[i] + recoil[i];
	}
}

static void add_radiation_pressure_one(
	struct CARandCtx* ctx,
	const double* hbar_k,
	double hbar_k_nrm,
	double nbar,
	double* f)
{
	int actual_n; 
	ca_rand_poisson(ctx, 1, nbar, &actual_n);
	if (actual_n > CA_LARGE_N) {
		add_radiation_pressure_large_n(ctx, hbar_k, hbar_k_nrm, actual_n, f);
	} else {
		add_radiation_pressure_small_n(ctx, hbar_k, hbar_k_nrm, actual_n, f);
	}
}

void ca_add_radiation_pressure(int n,
        struct CARandCtx* ctx, 
	const double* hbar_k,
	const double* nbars,
	double* f)
{
	double hbar_k_nrm = 0.0;
	int i;
	for (i = 0; i < 3; ++i) {
		hbar_k_nrm += SQR(hbar_k[i]);
	}
	hbar_k_nrm = sqrt(hbar_k_nrm);
	for (i = 0; i < n; ++i) {
		add_radiation_pressure_one(ctx, hbar_k, hbar_k_nrm, nbars[i], f + 3 * i);
	}
}
