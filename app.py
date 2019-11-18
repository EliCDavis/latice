import time
from sonar import Sonar
from gpiozero import OutputDevice, InputDevice, PWMOutputDevice
from proximity_blinking_controller import ProximityBlinkingController
import threading
from math import sqrt
import os

from telegram.ext import Updater
updater = Updater(token=os.environ['TELEGRAM_TOKEN'])

ECHO = InputDevice(18)
RIGHT_TRIGGER = OutputDevice(17)
MIDDLE_TRIGGER = OutputDevice(27)
LEFT_TRIGGER = OutputDevice(22)

LED_PINS = [16, 20, 21, 26, 6, 13, 19, 5]

currentControl = "proximity"

controllers = {
    "proximity": ProximityBlinkingController(len(LED_PINS), 0.3, 200.0)
}

# Using datasheet at: https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf
# "we suggest to use over 60ms measurement cycle, in order to prevent trigger
# signal to the echo signal".. whatever that means
READING_TIMEOUT_MS = 61

LED_CHANGE_RATE = .001


def distance_display(dist):
    if dist == -666:
        return "?"
    else:
        return "%.1f cm" % dist


stop_light_driver_thread = False

def light_controller_driver_thread():
    while True:

        pwms = []
        for controllerKey in controllers:
            if controllerKey == currentControl:
                pwms = controllers[controllerKey].get_pwm_values(time.time())
            else:
                controllers[controllerKey].get_pwm_values(time.time())
        
        for i in range(len(pwms)):
            if pwms[i] < .1:
                LED_OUT[i].value = 0
            else:
                LED_OUT[i].value = sqrt(pwms[i]-.1)
        time.sleep(LED_CHANGE_RATE)
        if stop_light_driver_thread:
            for i in range(len(LED_OUT)):
                LED_OUT[i].close()
            break


if __name__ == '__main__':

    light_controller_thread = threading.Thread(
        target=light_controller_driver_thread)
    light_controller_thread.start()

    left_sonar = Sonar(LEFT_TRIGGER, ECHO, READING_TIMEOUT_MS)
    middle_sonar = Sonar(MIDDLE_TRIGGER, ECHO, READING_TIMEOUT_MS)
    right_sonar = Sonar(RIGHT_TRIGGER, ECHO, READING_TIMEOUT_MS)

    LED_OUT = []
    for pin in LED_PINS:
        LED_OUT.append(PWMOutputDevice(pin))

    try:
        while True:
            left_dist = left_sonar.distance()
            time.sleep(.100)
            middle_dist = middle_sonar.distance()
            time.sleep(.100)
            right_dist = right_sonar.distance()
            time.sleep(.100)
            print("left: %s; middle: %s; right: %s;" %
                  (distance_display(left_dist), distance_display(middle_dist), distance_display(right_dist)))

            for controllerKey in controllers:
                controllers[controllerKey].set_sensor_values(
                    [left_dist, middle_dist, right_dist])

            time.sleep(1)

    except KeyboardInterrupt:
        ECHO.close()
        LEFT_TRIGGER.close()
        MIDDLE_TRIGGER.close()
        RIGHT_TRIGGER.close()
        stop_light_driver_thread = True
        print("Measurement stopped by User")
