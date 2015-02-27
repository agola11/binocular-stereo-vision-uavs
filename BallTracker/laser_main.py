#Laser Gimbal Main Program
#Bolling/Gola 2015
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.PWM as PWM
from math import sqrt
import serial

current_servo_x = 7.5
current_servo_y = 7.5
cp = .01
x_servo = "P9_14"
y_servo = "P9_16"
valid = 0
size_to_target = {1:(1,2),
                  2:(1,3),
                  3:(2,4)}

#repeatedly takes measurements with the laser...
def take_measurements():
    while(true):
        if(valid):
            ser.write("*00004#")
            for x in range(0,3):
                s = ser.readline()
                print(s)

# get ball position, change servo position accordingly
def track_ball():
    #Get Ball position
    x,y,size = 0,0,0
        
    #Calculate desired ball position based on distance
    size_int = int(round(size))
    (target_x,target_y) = size_to_target[size_int]
    x_err = x - target_x
    y_err = y - target_y

    #control shit
    current_servo_x += x_err*cp
    current_servo_y += y_err*cp
    current_servo_x = min(current_servo_x,10)
    current_servo_x = max(current_servo_x,5)
    current_servo_y = min(current_servo_y,10)
    current_servo_y = max(current_servo_y,5)

    #check if we're on target
    valid = sqrt(x_err**2 + y_err**2) < size


#Initialize Servo PWM control
PWM.start(x_servo,current_servo_x,50,0)
PWM.start(y_servo,current_servo_y,50,0)

#Initialize UART for laser data
UART.setup("UART1")
ser = serial.Serial(port = "/dev/ttyO1", baudrate=115200,timeout=1)
ser.close()
ser.open()

t = threading.Thread(target=take_measurements)
t.daemon = True
t.start()

while true:
    track_ball()
    PWM.set_duty_cycle(x_servo,current_servo_x)
    PWM.set_duty_cycle(y_servo,current_servo_y)

