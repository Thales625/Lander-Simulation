import numpy as np

class CelestialBody:
	def __init__(self, terrain_fun, gravity:float):
		self.terrain = terrain_fun # y(x)
		self.gravity = np.array([0., -gravity])
	
	def curve(self):
		x_arr = np.arange(self.terrain.min_x, self.terrain.max_x, 1)
		return x_arr, self.terrain(x_arr)

	def get_flat_spot(self, x0, x1):
		x_arr = np.linspace(x0, x1, 1000)
		y_arr = self.terrain(x_arr)

		slopes = np.abs(np.gradient(y_arr, x_arr))

		min_idx = np.argmin(slopes)

		return np.array([x_arr[min_idx], y_arr[min_idx]])
