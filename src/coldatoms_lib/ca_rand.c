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
	for (int i = 0; i < n; ++i) {
		x[i] = dsfmt_genrand_close_open(&ctx->dsfmt);
	}
}

static double generate_gaussian_random_number(struct CARandCtx* ctx, double mean, double std) {
	const double epsilon = DBL_EPSILON;
	const double two_pi = 2.0 * 3.14159265358979323846;

	static double z0, z1;
	static int generate = 0;
	generate = generate == 0 ? 1 : 0;

	if (!generate) {
		return z1 * std + mean;
	}

	double u1, u2;
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
	for (int i = 0; i < n; ++i) {
		x[i] = generate_gaussian_random_number(ctx, mean, std);
	}
}

#if 0
int blGeneratePoisson(double nbar) {
  static const double thresholdKnuth = 25.0;
  if (nbar < thresholdKnuth) {
    return blGeneratePoissonKnuth(nbar);
  } else {
    int sample;
    do {
      sample = round(blGenerateGaussianNoise(nbar, sqrt(nbar)));
    } while (sample < 0);
    return sample;
  }
}

#endif
