import numpy as np

from universe import Universe
from celestial_body import CelestialBody
from terrain import Terrain
from vessel import Vessel
from engine import Engine
from rcs import RCSEngine
from part import Part
from PDG import compute_tgo, compute_a0

from utils import rotate_vec2

celestial_body = CelestialBody(
	# terrain_fun=Terrain.from_sine_wave(seed=42, n_harmonics=5),
	terrain_fun=Terrain.from_file("terrain.npz"),
	gravity=1.62
)

universe = Universe(celestial_body)

# vessel
blue_ghost = Vessel(
	position=np.array([0.0, 500.0]),
	dry_mass=470.0,
	fuel_mass=1100.0,
	celestial_body=celestial_body,
	size=np.array([2.0, 3.5]),
	color="orange"
)

# engines
blue_ghost.add_engine(0.,
	Engine(
		vessel_reference_frame=blue_ghost.reference_frame,
		size=np.array([.4, .8]),
		max_thrust=5000.,
		max_angle=np.radians(30.)
	)
)
blue_ghost.add_engine(.55,
	Engine(
		vessel_reference_frame=blue_ghost.reference_frame,
		size=np.array([.4, .7]),
		max_thrust=1000.0,
		max_angle=np.radians(20.)
	)
)
blue_ghost.add_engine(-.55,
	Engine(
		vessel_reference_frame=blue_ghost.reference_frame,
		size=np.array([.4, .7]),
		max_thrust=1000.0,
		max_angle=np.radians(20.)
	)
)

# rcs
blue_ghost.add_rcs_engine(-1.3,
	RCSEngine(
		vessel_reference_frame=blue_ghost.reference_frame,
		rotation=np.radians(0.),
		size=np.array([.3, .4]),
		max_thrust=2000.
	),
	left=False
)
blue_ghost.add_rcs_engine(-1.3,
	RCSEngine(
		vessel_reference_frame=blue_ghost.reference_frame,
		rotation=np.radians(0.),
		size=np.array([.3, .4]),
		max_thrust=2000.
	),
	left=True
)

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
	zorder=6,
	reference_frame=blue_ghost.reference_frame
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
	zorder=6,
	reference_frame=blue_ghost.reference_frame
))

universe.vessels.append(blue_ghost)

### CONTROL

blue_ghost.position = np.array([1., 150.])
blue_ghost.velocity = np.array([0., 0.])

# target_spot = celestial_body.get_flat_spot(celestial_body.terrain.min_x, celestial_body.terrain.max_x)
target_spot = celestial_body.get_flat_spot_closest_to_vessel(blue_ghost.position[0], 10.)
# target_spot = celestial_body.get_spot(blue_ghost.position[0] + blue_ghost.velocity[0]*10.)
checkpoint_spot = target_spot + np.array([0., 10.])

# find minimum Tgo
Tgo = compute_tgo(blue_ghost.position-checkpoint_spot, blue_ghost.velocity, celestial_body.gravity[1], blue_ghost.available_thrust/blue_ghost.mass)

if not Tgo[1]:
	print("Not converge")
	exit()

Tgo = Tgo[0]

def setup_func():
	blue_ghost.control.throttle = 0.
	blue_ghost.auto_pilot.engage()

def loop_func(ut):
	t_go = Tgo - ut

	if t_go > 1.:
		ds = checkpoint_spot - blue_ghost.position

		a0 = compute_a0(t_go, checkpoint_spot - blue_ghost.position, blue_ghost.velocity, celestial_body.gravity)

		throttle = blue_ghost.mass*np.linalg.norm(a0) / blue_ghost.available_thrust

		blue_ghost.control.throttle = throttle

		a0[1] = -a0[1]
		blue_ghost.auto_pilot.target_direction = a0

		print(f"tgo: {t_go:.2f}\nthrottle: {throttle:.2f}\ndist: {np.linalg.norm(ds)}\n")
		return

	target_dir = -blue_ghost.velocity
	target_dir[1] = -np.abs(target_dir[1]) - 5.
	blue_ghost.auto_pilot.target_direction = target_dir

	delta_speed = -1. - blue_ghost.velocity[1]
	blue_ghost.control.throttle = (delta_speed - celestial_body.gravity[1]) / (blue_ghost.available_thrust/blue_ghost.mass)
	print(f"Vy: {blue_ghost.velocity[1]:.2f}")


# universe.plot_terrain()

universe.Simulate(setup_func, loop_func, target_spot, checkpoint_spot, blue_ghost.position)
# universe.SimulateGIF(setup_func, loop_func, 2.)