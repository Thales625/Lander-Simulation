import numpy as np
from random import random

from reference_frame import ReferenceFrame
from shapes import Polygon
from plume import Plume

class RCSEngine:
    def __init__(self, vessel_reference_frame, rotation, size:float, max_thrust, color="white") -> None:
        self.direction = np.array([1., 0.])

        self.reference_frame = ReferenceFrame(rotation)

        self.shape = Polygon(
            vertices=[
                size*np.array([0.5, 0.5]),
                size*np.array([0.0, -0.5]),
                size*np.array([-0.5, 0.5]),
            ],
            color=color,
            zorder=3
        )
        self.shape.reference_frame = vessel_reference_frame
        
        self.max_thrust = max_thrust

        # plume
        self.plume = Plume(
            vessel_reference_frame=vessel_reference_frame,
            nozzle_size=size,
            flame_length=3.5,
            color="gray"
        )
    
    def throttle(self, gimbal):
        if np.sign(self.direction[0]) == np.sign(gimbal): return abs(gimbal)
        return 0

    def update(self, gimbal):
        # update plume
        throttle = self.throttle(gimbal)
        self.plume.set_scale(throttle + ((random()*0.1) if throttle > 0. else 0.))
    
    def draw(self):
        self.shape.draw(self.reference_frame())
        self.plume.draw(self.reference_frame())