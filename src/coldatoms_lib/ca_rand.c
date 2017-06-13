#include <rand.h>

#if define(HAVE_MKL)
#elif defined(HAVE_SPRNG)
#else

#include <stdlib.h>


struct CARandCtx {};

void ca_rand_init()
{
}

void ca_rand_finalize()
{
}

CARandCtx ca_rand_create()
{
	return NULL;
}

void ca_rand_destroy(CARandCtx* ctx)
{
	*ctx = NULL;
}

void ca_rand_seed(CARandCtx ctx, int seed)
{
}

double ca_rand(CARandCtx ctx, int n, double* x)
{
	static const double max = RAND_MAX;
	for (int i = 0; i < n; ++i) {
		x[i] = rand() / max;
	}
}

void ca_irand(CARandCtx ctx, int n, int* a)
{
	for (int i = 0; i < n; ++i) {
		a[i] = rand();
	}
}

int ca_rand_max()
{
	return RAND_MAX;
}

#endif

