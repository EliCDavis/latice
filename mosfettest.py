import time
from gpiozero import PWMOutputDevice
import math

LED_PINS = [5, 6, 13, 19, 26, 16, 20, 21]

#OUT = 5

if __name__ == '__main__':
    #pin_out = PWMOutputDevice(OUT)

    OUTS = []
    for pin in LED_PINS:
        OUTS.append(PWMOutputDevice(pin))
    # pin_out.on()
    # time.sleep(2)
    # pin_out.off()
    #pin_out.blink(3, 3, 1, True)

    try:
        while True:
            time.sleep(.01)
            #pin_out.value = .888

            for i in range(len(OUTS)):
                OUTS[i].value = .888 * abs(math.sin(time.time() + (float(i)*.170)))
    except KeyboardInterrupt:
        print("Stopping")
