from math import sin
from light_controller import LightController


class TwinkleController(LightController):

    def __init__(self, num_lights, movement_speed):
        LightController.__init__(self, num_lights)
        self.__movement_speed = movement_speed

    def get_pwm_values(self, new_time):

        new_values = []

        for i in range(len(self._pwm_values)):
            new_values.append( .888 * abs(sin(new_time + (float(i)*.170)))) 

        return new_values
