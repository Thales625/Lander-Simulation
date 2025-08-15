import numpy as np

from reference_frame import ReferenceFrame
from shapes import Polygon

class Plume:
    def __init__(self, vessel_reference_frame, nozzle_size, flame_length=5.0, color="red"):
        self.shape = Polygon(
            vertices=[
                np.array([nozzle_size[0]*0.5, 0.0]),
                np.array([-nozzle_size[0]*0.5, 0.0]),
                np.array([0.0, flame_length]),
            ],
            color=color,
            edgecolor=None,
            zorder=20,
            reference_frame=vessel_reference_frame
        )

        self.reference_frame = ReferenceFrame(translation=np.array([0., nozzle_size[1]*.5]))

    def set_scale(self, scale:float):
        self.reference_frame.scale = np.array([1., scale])
    
    def draw(self, engine_transform):
        self.shape.draw(self.reference_frame() + engine_transform)
