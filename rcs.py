import numpy as np
from random import random

from reference_frame import ReferenceFrame
from shape import Shape
from plume import Plume

class RCSEngine:
    def __init__(self, rotation, size:float, max_thrust, color="white") -> None:
        self.direction = np.array([1., 0.])

        self.reference_frame = ReferenceFrame(rotation)

        self.shape = Shape(
            vertices=[
                size*np.array([0.5, 0.5]),
                size*np.array([0.0, -0.5]),
                size*np.array([-0.5, 0.5]),
            ],
            color=color,
            zorder=3
        )
        
        self.max_thrust = max_thrust

        self.plume = Plume(size, 3.5, "gray")
    
    def throttle(self, gimbal):
        if np.sign(self.direction[0]) == np.sign(gimbal): return abs(gimbal)
        return 0

    def update(self, gimbal):
        # update plume
        throttle = self.throttle(gimbal)
        self.plume.set_scale(throttle + ((random()*0.1) if throttle > 0. else 0.))
    
    def draw(self, ax, vessel_transform=None):
        self.shape.draw(ax, self.reference_frame() + vessel_transform)
        # self.plume.draw(ax,  vessel_transform)
        self.plume.draw(ax, self.reference_frame() + vessel_transform)