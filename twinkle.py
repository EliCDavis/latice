import time
from gpiozero import PWMOutputDevice
import math
import sys

# LED_PINS = [13, 6, 5, 19, 26, 16, 20, 21]

LED_PINS = [16, 20, 21, 26, 6, 13, 19, 5]


if __name__ == '__main__':

    OUTS = []
    for pin in LED_PINS:
        OUTS.append(PWMOutputDevice(pin))

    try:
        while True:
            time.sleep(.01)

            for i in range(len(OUTS)):
                OUTS[i].value = .888 * abs(math.sin(time.time() + (float(i)*.170)))

        # i = 0
        # while True:
        #     OUTS[i].value = .888
        #     val = raw_input()
        #     i = (i + 1) % len(LED_PINS)
        #     print(i)
        #     print("next")


    except KeyboardInterrupt:
        print("Stopping")
        for i in range(len(OUTS)):
                OUTS[i].close()
