from matplotlib.patches import Polygon
from matplotlib.transforms import Affine2D

class Shape:
    def __init__(self, vertices, color="blue", edgecolor="black", zorder=1):
        self.polygon = Polygon(vertices, closed=True, facecolor=color, edgecolor=edgecolor, zorder=zorder)

    def draw(self, ax, transform=Affine2D()):
        self.polygon.set_transform(transform + ax.transData)
    
    def setup(self, ax):
        ax.add_patch(self.polygon)