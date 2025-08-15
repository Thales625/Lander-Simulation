from shapes import Polygon

class Part:
    def __init__(self, position, vertices, color, zorder=6, reference_frame=None) -> None:
        self.shape = Polygon(
            vertices=vertices+position,
            color=color,
            zorder=zorder,
            reference_frame=reference_frame
        )
    
    def draw(self):
        self.shape.draw()