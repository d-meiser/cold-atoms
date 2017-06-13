#ifndef CA_RAND_H
#define CA_RAND_H

typedef struct CARandCtx* CARandCtx;

void ca_rand_init();
void ca_rand_finalize();
CARandCtx ca_rand_create();
void ca_rand_destroy(CARandCtx* ctx);
void ca_rand_seed(CARandCtx ctx, int seed);
void ca_rand(CARandCtx ctx, int n, double* x);
void ca_irand(CARandCtx ctx, int n, int* a);
int ca_rand_max();

#endif

