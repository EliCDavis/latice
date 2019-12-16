from math import sin
from light_controller import LightController
import os
import time


class SecurityController(LightController):

    def __init__(self, num_lights, camera, mutex, min_dist_cm, bot, chat_id):
        LightController.__init__(self, num_lights)
        self.__camera = camera
        self.__mutex = mutex
        self.__min_dist_cm = min_dist_cm
        self.__bot = bot
        self.__chat_id = chat_id

    def __send_alert(self):
        self.__mutex.acquire()

        self.__bot.send_message(
            chat_id=self.__chat_id,
            text="Sensor has been tripped in security mode! Starting video recording..."
        )

        try:
            self.__camera.start_recording('./video.h264')
            time.sleep(5)
            self.__camera.stop_recording()
            os.system('MP4Box -add video.h264 video.mp4')
            os.remove("video.h264")

            self.__bot.send_video(
                chat_id=self.__chat_id,
                video=open('./video.mp4', 'rb')
            )
            
            os.remove("video.h264")
            os.remove("video.mp4")
        except:
            self.__bot.send_message(
                chat_id=self.__chat_id,
                text="Issue taking recording. Try /picture or /video command!"
            )
            
        finally:
            self.__mutex.release()

    

    def get_pwm_values(self, new_time):

        # self._distance_readings

        send_alert = False
        for reading in self._distance_readings:
            if reading <= self.__min_dist_cm and reading > 0:
                send_alert = True

        if send_alert:
            self.__send_alert()


        return [0] * len(self._pwm_values)