from math import floor

class LightController:

    def __init__(self, numLights):
        self._pwm_values = [0] * numLights
        self._distance_readings = []

    def set_sensor_values(self, distance_readings):
        self._distance_readings = distance_readings

    def get_pwm_values(self, current_time):
        """ 
        Determine the intensity the lights should be at given the current time.
        """
        pass

    def _distance_to_pwm(self, distance_readings, num_lights, max_distance):

        if distance_readings is None or len(distance_readings) == 0:
            return []

        pwms = [0] * num_lights
        sensors_per_light = float(len(distance_readings)) / float(num_lights)

        for light_index in range(num_lights):
            accumlative_sensor_index = (light_index + 1) * sensors_per_light

            # if we meet an index exactly (check if this is proper for python)
            if accumlative_sensor_index.is_integer():
                dist = distance_readings[int(floor(accumlative_sensor_index)) - 1]
                if dist == -666:
                    pwms[light_index] = 0
                else: 
                    pwms[light_index] = (1.0 - (dist / max_distance))

            elif floor(accumlative_sensor_index) != floor(light_index * sensors_per_light):
                oneIndex = int(floor(accumlative_sensor_index)) - 1
                dist1 = 0
                if distance_readings[oneIndex] != -666:
                    dist1 = distance_readings[oneIndex]

                twoIndex = int(floor(accumlative_sensor_index))
                dist2 = 0
                if distance_readings[twoIndex] != -666:
                    dist2 = distance_readings[twoIndex]

                dist = (dist1 + dist2) * .5

                pwms[light_index] = 1.0 - (dist / max_distance)
            else:
                dist = distance_readings[int(floor(accumlative_sensor_index))]
                if dist == -666:
                    pwms[light_index] = 0
                else:
                    pwms[light_index] = 1.0 - (dist / max_distance)
        return pwms
