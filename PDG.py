import numpy as np

def compute_a0(t_go, ds, v, g):
    return ds*(6./(t_go**2)) - v*(4./t_go) - g

def compute_j0(t_go, ds, v):
    return (6/t_go**2)*v - (12/t_go**3)*ds

def is_valid_path(S, V, t_go, a_eng, g):
    Aeng = a_eng**2

    a0 = compute_a0(S, V, t_go, g)
    j0 = compute_j0(S, V, t_go)

    d1 = np.dot(a0, a0)

    if d1 > Aeng: return False

    d2 = np.dot(a0, j0)
    d3 = np.dot(j0, j0)

    if d1 - (d2**2 / d3) > Aeng: return False
    if d1 + 2*(-d2/d3)*d2 + d3*(-d2/d3)**2 > Aeng: return False

    if d1 + 2*t_go*d2 + d3*t_go**2 > Aeng: return False

    return True

def search_tgo(S, V, t_min, t_max, a_eng, g, dt=0.1):
    if t_min < 0: t_min = 1
    if t_max < t_min: t_max = t_min

    while t_min < t_max:
        if is_valid_path(S, V, t_min, a_eng, g):
            return (t_min, True)
        t_min += dt

    return (t_max, False) # no valid path! using TgoMax


def compute_tgo(ds, v, g, a_eng):
    min_tgo = -(2*v[1] + np.sqrt(4*v[1]**2 - 6*g*ds[1])) / g
    max_tgo = -3*ds[1]/v[1] if v[1] != 0 else 500

    if max_tgo < 0: max_tgo = min_tgo+500

    return search_tgo(ds, v, min_tgo, max_tgo, a_eng, g)