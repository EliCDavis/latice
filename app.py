import time
from sonar import Sonar
from gpiozero import OutputDevice, InputDevice

ECHO = InputDevice(26)

RIGHT_TRIGGER = OutputDevice(22)
MIDDLE_TRIGGER = OutputDevice(27)
LEFT_TRIGGER = OutputDevice(17)

# Using datasheet at: https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf
# "we suggest to use over 60ms measurement cycle, in order to prevent trigger
# signal to the echo signal".. whatever that means
READING_TIMEOUT_MS = 61


def distance_display(sonar):
    dist = sonar.distance()
    if dist == -666:
        return "?"
    else:
        return "%.1f cm" % dist


if __name__ == '__main__':

    left_sonar = Sonar(LEFT_TRIGGER, ECHO, READING_TIMEOUT_MS)
    middle_sonar = Sonar(MIDDLE_TRIGGER, ECHO, READING_TIMEOUT_MS)
    right_sonar = Sonar(RIGHT_TRIGGER, ECHO, READING_TIMEOUT_MS)

    try:
        while True:
            print("left: %s; middle: %s; right: %s;" %
                  (distance_display(left_sonar), distance_display(middle_sonar), distance_display(right_sonar)))
            time.sleep(1)

    except KeyboardInterrupt:
        ECHO.close()
        LEFT_TRIGGER.close()
        MIDDLE_TRIGGER.close()
        RIGHT_TRIGGER.close()
        print("Measurement stopped by User")
