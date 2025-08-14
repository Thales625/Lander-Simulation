import numpy as np
from random import random

from reference_frame import ReferenceFrame
from shape import Shape
from plume import Plume

class Engine:
    def __init__(self, size, max_thrust, max_angle=np.pi/4, color="black") -> None:
        self.position = np.array([0.0, 0.0]) # vessel reference frame
        self.angle = 0.0
        self.direction = np.array([0.0, 0.0])

        self.reference_frame = ReferenceFrame()

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
        self.max_angle = max_angle

        # plume
        self.plume = Plume(size)

    def update(self, throttle):
        # update reference frame
        self.reference_frame.rotation = self.angle
        self.reference_frame.translation = self.position

        # update plume
        self.plume.set_scale(throttle + ((random()*0.1) if throttle > 0. else 0.))
    
    def draw(self, ax, vessel_transform=None):
        self.shape.draw(ax, self.reference_frame() + vessel_transform)

        self.plume.draw(ax, self.reference_frame() + vessel_transform)
