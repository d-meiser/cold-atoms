#include <ca_rand.h>
#include <stdlib.h>
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
	dsfmt_fill_array_close_open(&ctx->dsfmt, x, n);
}

