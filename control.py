from utils import clamp

class Control:
    def __init__(self) -> None:
        self._throttle = 0.0
        self._gimbal = 0.0
    
    @property
    def gimbal(self):
        return self._gimbal

    @gimbal.setter
    def gimbal(self, gimbal):
        self._gimbal = clamp(gimbal, 1., -1.)


    @property
    def throttle(self):
        return self._throttle

    @throttle.setter
    def throttle(self, throttle):
        self._throttle = clamp(throttle, 1., 0.)