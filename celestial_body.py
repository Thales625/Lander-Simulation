import numpy as np

class CelestialBody:
	def __init__(self, terrain_fun, gravity:float):
		self.terrain = terrain_fun
		self.gravity = np.array([0., -gravity])
	
	def curve(self, start, stop, n):
		x_arr = np.linspace(start, stop, n)
		return x_arr, self.terrain(x_arr)