#include <ca_rand.h>
#include <stdlib.h>


struct CARandCtx {};


struct CARandCtx* ca_rand_create()
{
	return NULL;
}

void ca_rand_destroy(struct CARandCtx** ctx)
{
	*ctx = NULL;
}

void ca_rand_seed(struct CARandCtx* ctx, int seed)
{
	srand(seed);
}

void ca_rand(struct CARandCtx* ctx, int n, double* x)
{
	static const double max = RAND_MAX;
	for (int i = 0; i < n; ++i) {
		x[i] = rand() / max;
	}
}

