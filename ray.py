def propagate_ray(pos, dir, terrain_spline, n=100):
    s = pos.copy()

    # check extrapolate spline limits

    for i in range(n):
        h = s[1] - terrain_spline(s[0])
        if np.abs(h) < 0.1:
            return s

        s += dir * h

        # if s[0] < 0: return None
        # if s[0] > downrange: return None
    
    return None

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    from utils import vec2_from_angle, rotate_vec2

    from spline import SplineCubic
    from terrain import terrain
    
    downrange = 100.0

    x_arr = np.linspace(0.0, downrange, 100)
    y_arr_terrain = terrain(x_arr, 2)

    terrain_spline = SplineCubic(x_arr, y_arr_terrain)

    rocket_pos = np.array([80., 50.])
    rocket_dir = vec2_from_angle(-np.pi/4)
    
    theta_max = np.pi/4
    for theta in np.linspace(-theta_max, theta_max, 5):
        ray_dir = rotate_vec2(-rocket_dir, theta)

        hit = propagate_ray(rocket_pos, ray_dir, terrain_spline)

        if hit is not None:
            plt.plot(*hit, "x")

        plt.arrow(*rocket_pos, *(ray_dir*5))

    plt.arrow(*rocket_pos, *(rocket_dir*5), width=0.5, label="Rocket")

    plt.plot(x_arr, y_arr_terrain, label="Terrain")

    plt.ylim(0, downrange)
    plt.xlim(0, downrange)
    plt.legend()
    plt.tight_layout()
    plt.show()