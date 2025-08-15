from matplotlib.transforms import Affine2D

import numpy as np

class ReferenceFrame:
    def __init__(self, rotation=0.0, translation=np.array([0.0, 0.0]), scale=np.array([1.0, 1.0])):
        self.rotation = rotation
        self.translation = translation
        self.scale = scale

    def __call__(self):
        return Affine2D().rotate(self.rotation).scale(*self.scale).translate(*self.translation)
    
    def transform_direction_to_local(self, global_direction):
        return Affine2D().rotate(self.rotation).transform(global_direction)


    def transform_position_to_local(self, global_position):
        return Affine2D().scale(*self.scale).translate(*-self.translation).rotate(-self.rotation).transform(global_position)

    def transform_position_to_global(self, local_position):
        return Affine2D().rotate(self.rotation).scale(*self.scale).translate(*self.translation).transform(local_position)