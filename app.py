import time
from sonar import Sonar
from gpiozero import OutputDevice, InputDevice, PWMOutputDevice
from proximity_blinking_controller import ProximityBlinkingController
from twinkle_controller import TwinkleController
import threading
from math import sqrt
import os

import teletest

from telegram.ext import CommandHandler, Updater


ECHO = InputDevice(18)
RIGHT_TRIGGER = OutputDevice(17)
MIDDLE_TRIGGER = OutputDevice(27)
LEFT_TRIGGER = OutputDevice(22)

LED_PINS = [16, 20, 21, 26, 6, 13, 19, 5]

currentControl = "proximity"

controllers = {
    "proximity": ProximityBlinkingController(len(LED_PINS), 0.3, 200.0),
    "twinkle": TwinkleController(len(LED_PINS), 0.3)
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
                # run all the other controllers to make sure their keeping up
                # with their delta times properly
                controllers[controllerKey].get_pwm_values(time.time())
        
        for i in range(len(pwms)):
            if pwms[i] < .1:
                LED_OUT[i].value = 0
            else:
                # LED_OUT[i].value = sqrt(pwms[i]-.1)
                LED_OUT[i].value = pwms[i]

        time.sleep(LED_CHANGE_RATE)
        if stop_light_driver_thread:
            for i in range(len(LED_OUT)):
                LED_OUT[i].close()
            break


def set_mode_command(update, context):
    global currentControl
    if teletest.should_respond(update, context) == False:
        return

    command = teletest.remove_prefix(update.message.text, "/mode")
    return_message = "Unrecognized command"

    if command == "twinkle":
        print("Setting mode to twinkle")
        return_message = "Setting mode to twinkle"
        currentControl = "twinkle"

    elif command == "sleep":
        print("Setting mode to sleep")
        return_message = "Setting mode to sleep"

    elif command == "bug":
        print("Setting mode to lightning bug")
        return_message = "Setting mode to lightning bug"
        currentControl = "proximity"

    elif command == "security":
        print("Setting mode to security")
        return_message = "Setting mode to security"
        
    elif command == "":
        return_message = "Please Specify a mode [twinkle | bug | security | sleep]"
    else:
        print("Unrecognized command")

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=return_message
    )


def bot_driver_thread():
    updater = Updater(token=os.environ['TELEGRAM_TOKEN'], use_context=True)
    
    updater.dispatcher.add_handler(CommandHandler('picture', teletest.capture_picture_command))
    updater.dispatcher.add_handler(CommandHandler('video', teletest.capture_video_command))
    updater.dispatcher.add_handler(CommandHandler('mode', set_mode_command))

    updater.start_polling()

if __name__ == '__main__':

    light_controller_thread = threading.Thread(
        target=light_controller_driver_thread)
    light_controller_thread.start()

    bot_thread = threading.Thread(
        target=bot_driver_thread)
    bot_thread.start()

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
