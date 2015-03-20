
import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("P8_10",GPIO.OUT);
for x in range(0, 100):
    if(x%2 == 0):
        GPIO.output("P8_10",GPIO.HIGH)
    else:
        GPIO.output("P8_10",GPIO.LOW)
    print "blinking yo."
    time.sleep(0.1)

GPIO.cleanup()
