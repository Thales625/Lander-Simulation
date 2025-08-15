import matplotlib.patches as mpl_patches
from matplotlib.lines import Line2D as _Line2D
from matplotlib.artist import Artist as _Artist

class Shape:
    def __init__(self, artist: _Artist, reference_frame=None):
        self.artist = artist
        self.ax = None
        self.reference_frame = reference_frame

        self._added = False

    def setup(self, ax):
        if self._added: return

        if isinstance(self.artist, mpl_patches.Patch):
            ax.add_patch(self.artist)
        elif isinstance(self.artist, _Line2D):
            ax.add_line(self.artist)
        else:
            ax.add_artist(self.artist)
        self.ax = ax
        self._added = True

    def draw(self, transform=None):
        if self._added is False: return

        t = self.ax.transData

        if self.reference_frame is not None: t = self.reference_frame() + t
        if transform is not None: t = transform + t

        self.artist.set_transform(t)


class Polygon(Shape):
    def __init__(self, vertices, color="blue", edgecolor="black", zorder=1, reference_frame=None):
        super().__init__(mpl_patches.Polygon(vertices, closed=True, facecolor=color, edgecolor=edgecolor, zorder=zorder), reference_frame)

class Line(Shape):
    def __init__(self, start=(0., 0.), end=(0., 0.), color="black", linewidth=1.0, linestyle="-", zorder=2, reference_frame=None):
        self._start = start
        self._end = end
        super().__init__(_Line2D([self._start[0], self._end[0]], [self._start[1], self._end[1]], color=color, linewidth=linewidth, linestyle=linestyle, zorder=zorder), reference_frame)

    def set_start_pos(self, pos):
        self._start = pos
        self._update_data()

    def set_end_pos(self, pos):
        self._end = pos
        self._update_data()

    def _update_data(self):
        self.artist.set_data([self._start[0], self._end[0]], [self._start[1], self._end[1]])