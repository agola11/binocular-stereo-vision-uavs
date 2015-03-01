import Adafruit_BBIO.PWM as PWM
import time

PWM.start("P9_14",7.5,50,0)

i = 0
while 1:
    i = (i + 1)%100
    PWM.set_duty_cycle("P9_14",5 + 5*i/100.)
    time.sleep(.1)
