import numpy as np

from ray import Ray
from utils import vec2_from_angle

class LiDAR:
    def __init__(self, position, terrain_func, vessel_reference_frame, fov=np.pi/2, n=1):
        self.rays = []
        self.vessel_reference_frame = vessel_reference_frame

        for angle in np.linspace(-fov, fov, n) if n > 1 else [0.]:
            direction = vec2_from_angle(angle)
            self.rays.append(
                Ray(
                    position=position,
                    direction=direction,
                    reference_frame=self.vessel_reference_frame,
                    terrain=terrain_func
                )
            )

    def update(self, ut):
        for ray in self.rays:
            s = ray.propagate_ray()

            if s is not None:
                ray.set_color("green")
            else:
                ray.set_color("red")
    
    def draw(self):
        for ray in self.rays: ray.draw()

    def get_shapes(self):
        return [ray.shape for ray in self.rays]