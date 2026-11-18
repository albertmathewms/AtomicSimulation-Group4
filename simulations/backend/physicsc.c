#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void pair_forces(const double *restrict p, double *restrict f, int N, double rc, double k, double r0) {
    for (int i = 0; i < N * 3; i++) {
        f[i] = 0.0;
    }

    const double rc2 = rc * rc;

    for (int i = 0; i < N; i++) {
        const double px_i = p[i * 3 + 0];
        const double py_i = p[i * 3 + 1];
        const double pz_i = p[i * 3 + 2];

        for (int j = i + 1; j < N; j++) {
            const double dx = px_i - p[j * 3 + 0];
            const double dy = py_i - p[j * 3 + 1];
            const double dz = pz_i - p[j * 3 + 2];

            const double dist2 = dx * dx + dy * dy + dz * dz;

            if (dist2 <= rc2 && dist2 > 0.0) {
                const double dist = sqrt(dist2);
                const double magnitude = -k * (dist - r0);
                const double inv_dist = 1.0 / dist;

                const double fx = magnitude * dx * inv_dist;
                const double fy = magnitude * dy * inv_dist;
                const double fz = magnitude * dz * inv_dist;

                f[i * 3 + 0] = f[i * 3 + 0] + fx;
                f[i * 3 + 1] = f[i * 3 + 1] + fy;
                f[i * 3 + 2] = f[i * 3 + 2] + fz;

                f[j * 3 + 0] = f[j * 3 + 0] - fx;
                f[j * 3 + 1] = f[j * 3 + 1] - fy;
                f[j * 3 + 2] = f[j * 3 + 2] - fz;
            }
        }
    }
}

void drag_force(const double *restrict v, double *restrict fd, int N, double g) {
    const int total_coords = N * 3;
    for (int i = 0; i < total_coords; i++) {
        fd[i] = -g * v[i];
    }
}

void walls_reflect(double *p, double *v, int N, double l) {
    for (int i = 0; i < N; i++) {
        for (int dim = 0; dim < 3; dim++) {
            const int idx = i * 3 + dim;
            if (p[idx] < 0.0) {
                v[idx] = v[idx] * -1.0;
                p[idx] = 0.0;
            } else if (p[idx] > l) {
                v[idx] = v[idx] * -1.0;
                p[idx] = l;
            }
        }
    }
}

void step_once(double *restrict p, double *restrict v, double *restrict f, 
               int N, double m, double dt, double l, double rc, double k, double r0, double g) {
    pair_forces(p, f, N, rc, k, r0);

    const double dt_over_m = dt / m;
    const int total_coords = N * 3;

    for (int i = 0; i < total_coords; i++) {
        const double fd = -g * v[i];
        v[i] = v[i] + (f[i] + fd) * dt_over_m;
        p[i] = p[i] + v[i] * dt;
    }

    walls_reflect(p, v, N, l);
}

void run_simulation(double *p, double *v, double *f, double *phistory, 
                    int N, int t_steps, double m, double dt, double l, double rc, double k, double r0, double g) {
    const int stride = N * 3;
    for (int step = 0; step < t_steps; step++) {
        step_once(p, v, f, N, m, dt, l, rc, k, r0, g);
        
        double *dest = phistory + (step * stride);
        for (int i = 0; i < stride; i++) {
            dest[i] = p[i];
        }
    }
}