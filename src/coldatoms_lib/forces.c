#include <forces.h>
#include <stdio.h>
#include <math.h>


static double distance(const double *r, double delta) {
  double dist = 0.0;
  for (int i = 0; i < 3; ++i) {
    dist += r[i] * r[i];
  }
  dist += delta;
  return sqrt(dist);
}


void coulomb_force(const double* positions, double charge, int num_ptcls,
                   double delta, double k, double* forces) {
  k *= charge * charge;
  const double *r0 = positions;
  for (int i = 0; i < num_ptcls; ++i) {
    const double *r1 = positions;
    for (int j = 0; j < num_ptcls; ++j) {
      double r[3];
      for (int m = 0; m < 3; ++m) {
        r[m] = r0[m] - r1[m];
      }
      double dist = distance(r, delta);
      double dist_cubed = dist * dist * dist;
      for (int m = 0; m < 3; ++m) {
        forces[m] += k * r[m] / dist_cubed;
      }
      r1 += 3;
    }
    r0 += 3;
    forces += 3;
  }
}

void coulomb_force_per_particle_charges(
    const double* positions, const double* charge, int num_ptcls,
    double delta, double k, double* forces) {
  const double *r0 = positions;
  for (int i = 0; i < num_ptcls; ++i) {
    const double *r1 = positions;
    for (int j = 0; j < num_ptcls; ++j) {
      double r[3];
      for (int m = 0; m < 3; ++m) {
        r[m] = r0[m] - r1[m];
      }
      double dist = distance(r, delta);
      double dist_cubed = dist * dist * dist;
      for (int m = 0; m < 3; ++m) {
        forces[m] += k * charge[i] * charge[j] * r[m] / dist_cubed;
      }
      r1 += 3;
    }
    r0 += 3;
    forces += 3;
  }
}
