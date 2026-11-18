import numpy as np


def build_cell_linked_list(p, rc, cell, weight):
    """Build linked-list heads and next-particle links for the current positions."""
    nc = int(weight[1, 0])
    cell_size = rc * 1.01
    cell[:, :] = np.floor_divide(p, cell_size).astype(int)
    np.clip(cell, 0, nc - 1, out=cell)

    hno = (cell @ weight).astype(int).ravel()
    heads = np.full(nc ** 3, -1, dtype=int)
    links = np.full(p.shape[0], -1, dtype=int)

    for i in range(p.shape[0]):
        links[i] = heads[hno[i]]
        heads[hno[i]] = i

    return heads, links, hno


def distpairs(p, rc, cell, weight):
    n = p.shape[0]
    nc = int(weight[1, 0])
    heads, links, hno = build_cell_linked_list(p, rc, cell, weight)

    d = np.zeros((n, n, 3), dtype=p.dtype)
    dist = np.zeros((n, n), dtype=p.dtype)
    neighbours = np.zeros((n, n), dtype=bool)

    rc2 = rc * rc
    for i in range(n):
        ix, iy, iz = cell[i]
        for cz in range(max(0, iz - 1), min(nc, iz + 2)):
            for cy in range(max(0, iy - 1), min(nc, iy + 2)):
                for cx in range(max(0, ix - 1), min(nc, ix + 2)):
                    j = heads[cx + nc * (cy + nc * cz)]
                    while j != -1:
                        if j != i:
                            delta = p[i] - p[j]
                            r2 = np.dot(delta, delta)
                            if r2 > 0.0 and r2 <= rc2:
                                d[i, j] = delta
                                dist[i, j] = np.sqrt(r2)
                                neighbours[i, j] = True
                        j = links[j]

    return(d, dist, neighbours)
    
def pair_forces_loop(p, rc, k, r0,cell,weight):
    d, dist, neighbours = distpairs(p, rc,cell,weight)
    f = np.zeros_like(p)
    magnitude = ((-k*((dist) - r0))*neighbours)/(dist + 1e-12)
    unit_vector = d/(dist[:, :, np.newaxis] + 1e-12)
    force = (magnitude[:, :, np.newaxis])*unit_vector
    f = np.sum(force, axis=1)

    # for i in range (p.shape[0]):
    #     for j in range (i+1, p.shape[0]):
    #         if neighbours[i][j]==True:
    #             magnitude = -k*(dist[i][j] - r0) 
    #             unit_vector = d[i][j]/dist[i][j]
    #             force = magnitude*unit_vector
    #             f[i] += force
    #             f[j] -= force
    return(f)

def drag_force(v, g):
    fd=np.zeros_like(v)
    fd=-g*v

    return(fd)

def walls_reflect(p, v, l):
    for dim in range(3):
        hitp = p[:, dim] < 0
        v[hitp, dim] *= -1
        p[hitp, dim] = 0.0

        hitn = p[:, dim] > l
        v[hitn, dim] *= -1
        p[hitn, dim] = l

    return(p, v)

def step_once(p, v, m, dt, l, rc, k, r0,g,cell,weight):
    f = pair_forces_loop(p, rc, k, r0,cell,weight)
    fd=drag_force(v,g)
    a = (f+fd)/m
    v += a*dt
    p += v*dt
    p, v = walls_reflect(p, v, l)

    return(p,v)

def run_simulation(p, v, m, t, dt, l, rc, k, r0,g,cell,weight):
    phistory = np.zeros((t, p.shape[0], 3))
    for step in range(t):
        p, v = step_once(p, v, m, dt, l, rc, k, r0,g,cell,weight)
        phistory[step] = p

    return(phistory)