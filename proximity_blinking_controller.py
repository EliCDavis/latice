from math import sin
from light_controller import LightController


class ProximityBlinkingController(LightController):

    def __init__(self, num_lights, movement_speed, max_distance):
        LightController.__init__(self, num_lights)
        self.__last_time = 0.0
        self.__movement_speed = movement_speed
        self.__max_distance = max_distance

    def get_pwm_values(self, new_time):
        delta_time = new_time - self.__last_time

        new_values = self._distance_to_pwm(
            self._distance_readings, len(self._pwm_values), self.__max_distance)

        if new_values is None or len(new_values) == 0:
            return []

        for new_val_index in range(len(new_values)):
            val = float(new_values[new_val_index]) + (new_values[new_val_index] * sin((new_time * 5.0) + (new_val_index * 10.0)))
            new_values[new_val_index] = max(min(val, 1.0), 0.0)

        for pwm_val_index in range(len(self._pwm_values)):
            if abs(new_values[pwm_val_index] - self._pwm_values[pwm_val_index]) < self.__movement_speed * delta_time:
                self._pwm_values[pwm_val_index] = new_values[pwm_val_index]
            else:
                direction = 1 if new_values[pwm_val_index] > self._pwm_values[pwm_val_index] else -1
                self._pwm_values[pwm_val_index] = self._pwm_values[pwm_val_index] + (self.__movement_speed * delta_time * direction)
            
        self.__last_time = new_time
        return self._pwm_values
