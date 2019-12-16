from math import sin
from light_controller import LightController


class SleepController(LightController):

    def __init__(self, num_lights):
        LightController.__init__(self, num_lights)

    def get_pwm_values(self, new_time):
        return [0] * len(self._pwm_values)
