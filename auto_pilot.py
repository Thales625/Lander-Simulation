from utils import *

class AutoPilot:
    def __init__(self, vessel) -> None:
        self.vessel = vessel
        self.target_direction = np.array([0., -1.])
        self.engaged = False
    
    @property
    def target_angle(self):
        return angle_from_vec2(self.target_direction)

    @target_angle.setter
    def target_angle(self, angle):
        self.target_direction = vec2_from_angle(angle)
    
    def engage(self):
        self.engaged = True

    def disengage(self):
        self.engaged = False

    def update(self, dt):
        if self.engaged:
            throttle = self.vessel.control.throttle

            target_direction = normalized(self.vessel.reference_frame.transform_direction_to_local(self.target_direction)) # vessel ref
            
            angle_delta = np.asin(target_direction[0])

            accel_ang_max = self.vessel.available_torque / self.vessel.moment_of_inertia

            alpha_target = np.sqrt(2 * np.abs(angle_delta) * accel_ang_max * throttle * 0.4) * sign(angle_delta)
            alpha_delta = alpha_target - self.vessel.angular_velocity
            accel_ang_target = -alpha_delta * 2

            self.vessel.control.gimbal = (accel_ang_target / (accel_ang_max * throttle)) if throttle != 0 else 0

            '''
            v = -self.vel.normalize()
            v.y = -abs(v.y) * 2
            self.target_angle = angle_from_vec2(v)

            accel_ang_max = self.available_torque / self.moi

            angle_delta = self.target_angle - self.angle
            v_target = sqrt(2 * abs(angle_delta) * accel_ang_max * self.throttle * 0.4) * sign(angle_delta)
            v_delta = v_target - self.vel_ang
            accel_ang_target = -v_delta * 2

            self.gimbal = (accel_ang_target / (accel_ang_max * self.throttle)) if self.throttle != 0 else 0
            '''