#ifndef CA_RAND_H
#define CA_RAND_H

struct CARandCtx;


struct CARandCtx* ca_rand_create(void);
void ca_rand_destroy(struct CARandCtx** ctx);
void ca_rand_seed(struct CARandCtx* ctx, int seed);
void ca_rand(struct CARandCtx* ctx, int n, double* x);

#endif

