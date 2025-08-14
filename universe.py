import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

class Universe:
    def __init__(self, celestial_body) -> None:
        self.vessels = []
        self.parts = []
        self._shapes = []

        self.active_vessel = None
        self.celestial_body = celestial_body

    def PhysicsLoop(self, dt):
        for vessel in self.vessels:
            vessel.update(dt, self.celestial_body)

    def RenderLoop(self, ax):
        for vessel in self.vessels:
            vessel.draw(ax)
        
        for part in self.parts:
            part.shape.draw(ax)
        
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
    
    def GetPolygons(self):
        return [shape.polygon for shape in self._shapes]


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
        # plt.legend()
        plt.tight_layout()

        ani.save(path, writer=PillowWriter(fps=int(1/dt)))

    def Simulate(self, setup_func, loop_func, dt=0.01):
        fig, ax = plt.subplots()

        self.UpdateShapes()
        self.SetupShapes(ax)

        polygons = self.GetPolygons()

        setup_func()

        def update(frame):
            loop_func(frame*dt)

            self.PhysicsLoop(dt)
            self.RenderLoop(ax)

            return polygons

        ani = FuncAnimation(fig, update, interval=dt*1000, blit=True, cache_frame_data=False)

        ax.set_xlim(-30., 30.)
        ax.set_ylim(-10., 60.)
        ax.set_aspect("equal", adjustable="datalim")

        plt.plot(*self.celestial_body.curve(-500, 500, 1000))
        plt.title("PDG Simulation")
        plt.grid()
        # plt.legend()
        plt.tight_layout()

        plt.show()