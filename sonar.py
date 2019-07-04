from gpiozero import OutputDevice, InputDevice
import threading
import time

class Sonar:

    def __init__(self, trigger_pin, echo_pin, timeout):
        self.__trigger_pin = OutputDevice(trigger_pin)
        self.__echo_pin = InputDevice(echo_pin)
        self.__timeout = timeout

    def __exceeded_timeout(self, start_time):
        return (time.time() - start_time) * 1000 > self.__timeout

    def distance(self):

        # Send a trigger pulse
        self.__trigger_pin.on()
        time.sleep(0.00001)
        self.__trigger_pin.off()

        distance_read_start_time = time.time()
        pulse_start_time = time.time()
        pulse_stop_time = time.time()

        while self.__echo_pin.value == 0 and self.__exceeded_timeout(distance_read_start_time) is False:
            pulse_start_time = time.time()

        # save time of arrival
        while self.__echo_pin.value == 1 and self.__exceeded_timeout(distance_read_start_time) is False:
            pulse_stop_time = time.time()

        return ((pulse_stop_time - pulse_start_time) * 34300) / 2
