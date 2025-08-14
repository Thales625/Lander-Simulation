import numpy as np
import matplotlib.pyplot as plt

def terrain(x, seed=0):
    np.random.seed(seed)

    n_harmonics = 5

    f = np.zeros_like(x)

    for _ in range(n_harmonics):
        A = np.random.uniform(1, 1.05)   # height
        B = np.random.uniform(0.05, 0.5) # frequency
        C = np.random.uniform(0.0, 2*np.pi) # phase
        f += A * (np.sin(B * x + C) + 1)
    
    return f

if __name__ == "__main__":
    downrange = 100.0
    dx = 1.0

    x_arr = np.arange(0.0, downrange, dx)
    y_arr = terrain(x_arr)

    plt.plot(x_arr, y_arr)

    # plt.axhline(0, linestyle="--")

    plt.ylim(0, downrange)
    plt.xlim(0, downrange)

    # plt.gca().set_aspect('equal', adjustable='datalim')
    # plt.show()

    safe_range = 5.0 # rocket base

    # fun = lambda x: # integrate x to x+safe_range

    # minimize_scalar()

    plt.plot(x_arr[:-1], np.abs(np.diff(y_arr)))
    plt.show()