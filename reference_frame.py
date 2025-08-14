from matplotlib.transforms import Affine2D

import numpy as np

class ReferenceFrame:
    def __init__(self, rotation=0.0, translation=np.array([0.0, 0.0]), scale=np.array([1.0, 1.0])):
        self.rotation = rotation
        self.translation = translation
        self.scale = scale

    def __call__(self):
        return Affine2D().rotate(self.rotation).scale(*self.scale).translate(*self.translation)
    
    def transform_direction(self, direction):
        return Affine2D().rotate(self.rotation).transform(direction)