import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

class Universe:
    def __init__(self, celestial_body) -> None:
        self.vessels = []
        self.parts = []
        self._shapes = []

        self.celestial_body = celestial_body

    def PhysicsLoop(self, dt, ut):
        for vessel in self.vessels:
            vessel.update(dt, ut)

    def RenderLoop(self):
        for vessel in self.vessels:
            vessel.draw()
        
        for part in self.parts:
            part.draw()
        
    def UpdateShapes(self):
        self._shapes = []

        for v in self.vessels:
            self._shapes.append(v.shape)

            for part in v.parts:
                self._shapes.append(part.shape)

            for engine in v.engines:
                self._shapes.append(engine.shape)
                self._shapes.append(engine.plume.shape)

            for rcs in v.rcs_engines:
                self._shapes.append(rcs.shape)
                self._shapes.append(rcs.plume.shape)

        for part in self.parts: self._shapes.append(part.shape)
    
    def SetupShapes(self, ax):
        for shape in self._shapes: shape.setup(ax)
    
    def GetArtists(self):
        return [shape.artist for shape in self._shapes]


    # TODO fix based on Simulate()
    def SimulateGIF(self, setup_func, loop_func, duration, dt=0.1, path="simulation.gif"):
        fig, ax = plt.subplots()

        self.UpdateShapes()
        self.SetupShapes(ax)

        polygons = self.GetPolygons()

        setup_func()

        def update(frame):
            ut = frame*dt

            print(f"{100*ut/duration:.0f}%")

            loop_func(ut)

            self.PhysicsLoop(dt)
            self.RenderLoop(ax)

            return polygons

        ani = FuncAnimation(fig, update, frames=int(duration/dt), interval=dt*1000, blit=True, cache_frame_data=False)

        ax.set_xlim(-30., 30.)
        ax.set_ylim(-10., 60.)
        ax.set_aspect("equal", adjustable="datalim")

        plt.plot(*self.celestial_body.curve(-500, 500, 1000))
        plt.title("PDG Simulation")
        plt.grid()
        plt.tight_layout()

        ani.save(path, writer=PillowWriter(fps=int(1/dt)))

    def Simulate(self, setup_func, loop_func, target_spot, checkpoint_spot, camera_pos, D=20., dt=0.01):
        fig, ax = plt.subplots()

        self.UpdateShapes()
        self.SetupShapes(ax)
        artists = self.GetArtists()

        setup_func()

        def update(frame):
            ut = frame*dt
            loop_func(ut)

            self.PhysicsLoop(dt, ut)
            self.RenderLoop()

            return artists

        ani = FuncAnimation(fig, update, interval=dt*1000, blit=True, cache_frame_data=False)

        # ax.set_xlim(camera_pos[0]-D, camera_pos[0]+D)
        # ax.set_ylim(camera_pos[1]-D, camera_pos[1]+D)
        ax.set_aspect("equal", adjustable="datalim")

        ax.plot(*target_spot, "x", color="red", label="Target spot landing")
        # ax.plot(*checkpoint_spot, "x", color="blue", label="Checkpoint")

        ax.plot(*self.celestial_body.curve(), c="gray")
        ax.plot(*self.celestial_body.get_points(), "o", c="gray")
        plt.title("PDG Simulation")
        plt.grid()
        plt.tight_layout()

        plt.show()
       
    def plot_terrain(self):
        fig, ax = plt.subplots()
        ax.set_aspect("equal", adjustable="datalim")
        ax.plot(*self.celestial_body.curve(), label="Terrain", c="black")
        ax.plot(*self.celestial_body.get_points(), "o", c="black")
        for x in self.celestial_body.get_points()[0]: ax.axvline(x, linestyle="--", color="black")
        plt.title("Terrain")
        plt.grid()
        plt.tight_layout()
        plt.legend()
        plt.show()