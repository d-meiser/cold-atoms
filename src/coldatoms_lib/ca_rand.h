#ifndef CA_RAND_H
#define CA_RAND_H

typedef struct CARandCtx* CARandCtx;

void ca_rand_init(void);
void ca_rand_finalize(void);
CARandCtx ca_rand_create(void);
void ca_rand_destroy(CARandCtx* ctx);
void ca_rand_seed(CARandCtx ctx, int seed);
void ca_rand(CARandCtx ctx, int n, double* x);
void ca_irand(CARandCtx ctx, int n, int* a);
int ca_rand_max(void);

#endif

