import numpy as np

HALF_PI = 0.5 * np.pi
TWO_PI = 2.0 * np.pi

def clamp(v, _max, _min):
    if v > _max: return _max
    if v < _min: return _min
    return v

def sign(v):
    if v < 0.0: return -1.0
    return 1.0

# vector
def vec2_from_angle(theta):
    return np.array([-np.sin(theta), np.cos(theta)])

def angle_from_vec2(vec):
    return np.atan2(vec[0], -vec[1])

def rotate_vec2(vecs, theta):
    rot = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

    vecs = np.asarray(vecs)

    if vecs.ndim == 1 and vecs.shape[0] == 2:
        return rot @ vecs
    elif vecs.ndim == 2 and vecs.shape[1] == 2:
        return vecs @ rot.T
    else:
        raise ValueError("invalid vec shape")

def normalized(vec):
    norm = np.linalg.norm(vec)

    if norm == 0: norm = 1e-3

    return vec / norm