import numpy as np

from shapes import Line

class Ray:
    def __init__(self, position, direction, reference_frame, terrain):
        self.position = position
        self.direction = direction
        self.shape = Line(
            start=self.position,
            end=self.position,
            color="green",
            reference_frame=reference_frame,
            zorder=1,
            linestyle="--"
        )
        self.reference_frame = reference_frame
        self.terrain = terrain

    def set_color(self, color):
        self.shape.artist.set_color(color)

    def draw(self):
        self.shape.draw()
    
    def propagate_ray(self, n=20, m=0.5):
        s = self.reference_frame.transform_position_to_global(self.position)
        d = self.reference_frame.transform_direction_to_local(self.direction)

        for i in range(n):
            h = s[1] - self.terrain(s[0])
            if np.abs(h) < m:
                self.shape.set_end_pos(self.reference_frame.transform_position_to_local(s))
                # self.shape.set_end_pos(self.position + self.direction*t)
                return s
            s += d * h
        
        return None