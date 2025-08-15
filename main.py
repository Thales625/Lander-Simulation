import numpy as np

from universe import Universe
from celestial_body import CelestialBody
from terrain import terrain
from vessel import Vessel
from engine import Engine
from rcs import RCSEngine
from part import Part

from utils import rotate_vec2

celestial_body = CelestialBody(lambda x: terrain(x, 0), 1.62)

universe = Universe(celestial_body)

# vessel
blue_ghost = Vessel(
	position=np.array([0.0, 50.0]),
	dry_mass=470.0,
	fuel_mass=1100.0,
	gravity=celestial_body.gravity,
	size=np.array([2.0, 3.5]),
	color="orange"
)

# engines
blue_ghost.add_engine(0.,
	Engine(
		size=np.array([.4, .7]),
		max_thrust=10000.,
		max_angle=np.radians(20.)
	)
)
blue_ghost.add_engine(.5,
	Engine(
		size=np.array([.4, .7]),
		max_thrust=1000.0,
		max_angle=np.radians(20.)
	)
)
blue_ghost.add_engine(-.5,
	Engine(
		size=np.array([.4, .7]),
		max_thrust=1000.0,
		max_angle=np.radians(20.)
	)
)

# rcs
blue_ghost.add_rcs_engine(-1.3,
	RCSEngine(
		rotation=np.radians(0.),
		size=np.array([.3, .4]),
		max_thrust=1000.0
	),
	left=False
)
blue_ghost.add_rcs_engine(-1.3,
	RCSEngine(
		rotation=np.radians(0.),
		size=np.array([.3, .4]),
		max_thrust=1000.0
	),
	left=True
)

# landing pad
universe.parts.append(Part(
	position=(lambda x: np.array([x, universe.celestial_body.terrain(x)]))(10.),
	vertices=np.array([
		np.array([-.5, -.5]),
		np.array([ .5, -.5]),
		np.array([ .5,  .5]),
		np.array([-.5,  .5])
	]) * np.array([10., 5.]),
	color="gray",
	zorder=4
))

# landing legs
w = 0.05
h1 = 0.05
h2 = 1.0
c = "yellow"
angle = np.pi/5
blue_ghost.parts.append(Part(
	position=blue_ghost.size*0.5,
	vertices=rotate_vec2([
		np.array([-w, -h1]),
		np.array([w, -h1]),
		np.array([w, h2]),
		np.array([-w, h2]),
	], -angle),
	color=c,
	zorder=6
))

blue_ghost.parts.append(Part(
	position=blue_ghost.size*np.array([-0.5, 0.5]),
	vertices=rotate_vec2([
		np.array([-w, -h1]),
		np.array([w, -h1]),
		np.array([w, h2]),
		np.array([-w, h2]),
	], angle),
	color=c,
	zorder=6
))

# another lander
lander = Vessel(
	position=np.array([0.0, 30.0]),
	dry_mass=470.0,
	fuel_mass=1100.0,
	gravity=celestial_body.gravity,
	size=np.array([2.0, 3.5]),
	color="lightsteelblue"
)

lander.add_engine(0.,
	Engine(
		size=np.array([.4, .7]),
		max_thrust=10000.,
		max_angle=np.radians(20.)
	)
)


universe.vessels.append(blue_ghost)
universe.vessels.append(lander)

def setup_func():
	blue_ghost.angle = -np.pi/2
	blue_ghost.velocity = np.array([0., 0.])

	blue_ghost.control.throttle = .4
	blue_ghost.auto_pilot.engage()

	# ---------

	lander.velocity = np.array([4., 0.])
	lander.control.throttle = .4
	lander.control.gimbal = 1.
	lander.auto_pilot.engage()

def loop_func(ut):
	target_dir = -blue_ghost.velocity
	target_dir[1] = -(np.abs(target_dir[1]) + 5)
	# target_dir = np.array([0., -1.])

	blue_ghost.auto_pilot.target_direction = target_dir

	# ---------

	target_dir_2 = -lander.velocity
	target_dir_2[1] = -(np.abs(target_dir_2[1]) + 5)
	lander.auto_pilot.target_direction = target_dir_2

universe.Simulate(setup_func, loop_func)
# universe.SimulateGIF(setup_func, loop_func, 2.)