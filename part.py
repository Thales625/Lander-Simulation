from shapes import Polygon

class Part:
    def __init__(self, position, vertices, color, zorder=6) -> None:
        self.shape = Polygon(
            vertices=vertices+position,
            color=color,
            zorder=zorder
        )
    
    def draw(self, vessel_transform=None):
        self.shape.draw(vessel_transform)