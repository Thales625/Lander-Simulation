from utils import *
from control import Control
from auto_pilot import AutoPilot

from reference_frame import ReferenceFrame
from shape import Shape
    
def get_torque(force, position): return force[0] * position[1] - force[1] * position[0]

class Vessel:
    def __init__(self, position, dry_mass, fuel_mass, moi=None, size=np.array([20., 80.]), color="gray") -> None:
        self.position = position
        self.velocity = np.array([0., 0.])
        self.angle = np.pi
        self.angular_velocity = 0.

        self.dry_mass = dry_mass
        self.fuel_mass = fuel_mass

        self.moment_of_inertia = moi or (.25 * self.mass * size.dot(size)) # moi approximation

        self.available_thrust = 0.
        self.available_torque = 0.

        self.reference_frame = ReferenceFrame(self.angle, self.position)

        # shape
        self.size = size
        self.shape = Shape(
            vertices=[
                self.size*np.array([.5, .5]),
                self.size*np.array([-.5, .5]),
                self.size*np.array([-.5, -.5]),
                self.size*np.array([.5, -.5])
            ],
            color=color,
            zorder=5
        )

        self.engines = []
        self.rcs_engines = []
        self.parts = []

        self.control = Control()
        self.auto_pilot = AutoPilot(self)
    
    @property
    def mass(self):
        return self.dry_mass + self.fuel_mass

    def add_engine(self, x_offset, engine):
        engine.position = self.size*np.array([0., .5]) + np.array([x_offset, 0.])
        self.engines.append(engine)

        self.update_forces()

    def add_rcs_engine(self, y_offset, rcs, left=True):
        rcs.reference_frame.translation = self.size*np.array([.5 if left else -.5, 0.]) + np.array([0., y_offset])

        rcs.reference_frame.rotation += np.radians(90.)
        if (left): rcs.reference_frame.rotation += np.pi

        rcs.direction = vec2_from_angle(rcs.reference_frame.rotation)

        self.rcs_engines.append(rcs)

        self.update_forces()

    def update_forces(self):
        self.available_thrust = 0.
        self.available_torque = 0.
        for engine in self.engines:
            self.available_thrust += engine.max_thrust
            self.available_torque += get_torque(vec2_from_angle(engine.max_angle) * engine.max_thrust, engine.position)

        for rcs_engine in self.rcs_engines:
            force = rcs_engine.direction * rcs_engine.max_thrust

            self.available_thrust += force[1]
            self.available_torque += get_torque(force, rcs_engine.reference_frame.translation)

        self.available_torque = abs(self.available_torque)

    def update(self, dt, celestial_body):
        # update engines
        for engine in self.engines:
            # control 
            engine.angle = self.control.gimbal * engine.max_angle

            engine.direction = -vec2_from_angle(self.angle + engine.angle)
            engine.update(self.control.throttle)
        
        # update rcs
        for rcs in self.rcs_engines:
            rcs.update(self.control.gimbal)

        # update vessel
        torque = 0.
        force = np.array([0., 0.])

        for engine in self.engines:
            f = engine.max_thrust * self.control.throttle
            force += f * engine.direction
            torque += get_torque(f * vec2_from_angle(engine.angle), engine.position)

        for rcs_engine in self.rcs_engines:
            f = rcs_engine.max_thrust * rcs_engine.throttle(self.control.gimbal)
            force -= f * rotate_vec2(rcs_engine.direction, self.angle)
            torque += get_torque(f*rcs_engine.direction, rcs_engine.reference_frame.translation)

        accel = -celestial_body.gravity + force / self.mass
        accel_ang = torque / self.moment_of_inertia

        self.angular_velocity += accel_ang * dt
        self.velocity += accel * dt

        self.angle = (self.angle + self.angular_velocity * dt)
        self.position += self.velocity * dt

        # auto pilot
        self.auto_pilot.update(dt)

        # update reference frame
        self.reference_frame.rotation = self.angle
        self.reference_frame.translation = self.position

		# clamp
        if self.angle > TWO_PI: self.angle = 0.
        elif self.angle < -TWO_PI: self.angle = 0.

    def draw(self, ax):
        transform = self.reference_frame()

        self.shape.draw(ax, transform)
    
        for engine in self.engines:
            engine.draw(ax, transform)

        for rcs_engine in self.rcs_engines:
            rcs_engine.draw(ax, transform)

        for part in self.parts:
            part.draw(ax, transform)