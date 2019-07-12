import time
from gpiozero import OutputDevice

OUT = 26


if __name__ == '__main__':

  pin_out = OutputDevice(OUT)

  pin_out.on()

  time.sleep(1)

  pin_out.off()
