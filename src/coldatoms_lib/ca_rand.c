#include <ca_rand.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>
#include <dSFMT/dSFMT.h>


struct CARandCtx {
	dsfmt_t dsfmt;
};


struct CARandCtx* ca_rand_create()
{
	struct CARandCtx* ctx = malloc(sizeof(*ctx));
	ca_rand_seed(ctx, 0);
	return ctx;
}

void ca_rand_destroy(struct CARandCtx** ctx)
{
	free(*ctx);
	*ctx = NULL;
}

void ca_rand_seed(struct CARandCtx* ctx, int seed)
{
	dsfmt_init_gen_rand(&ctx->dsfmt, seed);
}

void ca_rand(struct CARandCtx* ctx, int n, double* x)
{
	int i;
	for (i = 0; i < n; ++i) {
		x[i] = dsfmt_genrand_close_open(&ctx->dsfmt);
	}
}

static double generate_gaussian_random_number(struct CARandCtx* ctx, double mean, double std)
{
	const double epsilon = DBL_EPSILON;
	const double two_pi = 2.0 * 3.14159265358979323846;
	double u1, u2;

	static double z0, z1;
	static int generate = 0;
	generate = generate == 0 ? 1 : 0;

	if (!generate) {
		return z1 * std + mean;
	}

	do {
		u1 = dsfmt_genrand_close_open(&ctx->dsfmt);
		u2 = dsfmt_genrand_close_open(&ctx->dsfmt);
	} while ( u1 <= epsilon );

	z0 = sqrt(-2.0 * log(u1)) * cos(two_pi * u2);
	z1 = sqrt(-2.0 * log(u1)) * sin(two_pi * u2);
	return z0 * std + mean;
}


void ca_rand_gaussian(struct CARandCtx* ctx, int n, double mean, double std,
	double* x)
{
	int i;
	for (i = 0; i < n; ++i) {
		x[i] = generate_gaussian_random_number(ctx, mean, std);
	}
}
	
static int generate_poisson_knuth(struct CARandCtx* ctx, double lambda) {
	double L = exp(-lambda);
	int k = 0;
	double p = 1.0;
	do {
		++k;
		p *= dsfmt_genrand_close_open(&ctx->dsfmt);
	} while (p > L);
	return k - 1;
}

int generate_poisson_random_number(struct CARandCtx* ctx, double nbar) {
	static const double threshold_knuth = 25.0;
	int sample;
	if (nbar < threshold_knuth) {
		return generate_poisson_knuth(ctx, nbar);
	} else {
		do {
			sample = generate_gaussian_random_number(
				ctx, nbar, sqrt(nbar)) + 0.5;
		} while (sample < 0);
		return sample;
	}
}

void ca_rand_poisson(struct CARandCtx* ctx, int n, double nbar, int* x)
{
	int i;
	for (i = 0; i < n; ++i) {
		x[i] = generate_poisson_random_number(ctx, nbar);
	}
}

