import numpy as np
from scipy.optimize import minimize_scalar

class CelestialBody:
    def __init__(self, terrain_fun, gravity:float):
        self.terrain = terrain_fun # y(x)
        self.gravity = np.array([0., -gravity])
    
    def get_points(self):
        return self.terrain.x, self.terrain.y

    def curve(self):
        x_arr = np.arange(self.terrain.min_x, self.terrain.max_x, 1.)
        return x_arr, self.terrain(x_arr)

    def get_spot(self, x):
        return np.array([x, self.terrain(x)])

    def get_flat_spot(self, x_min, x_max):
        def slope_cost(x):
            dx = 0.1
            y1 = self.terrain(x - dx)
            y2 = self.terrain(x + dx)
            slope = (y2 - y1) / (2*dx)
            return np.abs(slope)

        res = minimize_scalar(slope_cost, bounds=(x_min, x_max), method='bounded')
        x_best = res.x
        y_best = self.terrain(x_best)

        return np.array([x_best, y_best])