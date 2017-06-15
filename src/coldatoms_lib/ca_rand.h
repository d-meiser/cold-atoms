#ifndef CA_RAND_H
#define CA_RAND_H

struct CARandCtx;


void ca_rand_init(void);
void ca_rand_finalize(void);
struct CARandCtx* ca_rand_create(void);
void ca_rand_destroy(struct CARandCtx** ctx);
void ca_rand_seed(struct CARandCtx* ctx, int seed);
void ca_rand(struct CARandCtx* ctx, int n, double* x);
void ca_irand(struct CARandCtx* ctx, int n, int* a);
int ca_rand_max(void);

#endif

