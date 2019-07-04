import time
from sonar import Sonar

RIGHT_TRIGGER = 17
RIGHT_ECHO = 27

MIDDLE_TRIGGER = 10
MIDDLE_ECHO = 9

LEFT_TRIGGER = 5
LEFT_ECHO = 6

READING_TIMEOUT_MS = 200

if __name__ == '__main__':

    left_sonar = Sonar(LEFT_TRIGGER, LEFT_ECHO, READING_TIMEOUT_MS)
    middle_sonar = Sonar(MIDDLE_TRIGGER, MIDDLE_ECHO, READING_TIMEOUT_MS)
    right_sonar = Sonar(RIGHT_TRIGGER, RIGHT_ECHO, READING_TIMEOUT_MS)

    try:
        while True:
            l_dist = left_sonar.distance()
            m_dist = middle_sonar.distance()
            r_dist = right_sonar.distance()

            print("left: %.1f cm; middle: %.1f cm; right: %.1f cm; " % (l_dist, m_dist, r_dist))
            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
