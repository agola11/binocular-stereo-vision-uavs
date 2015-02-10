
import Adafruit_BBIO.UART as UART
import serial

UART.setup("UART1")

ser = serial.Serial(port = "/dev/ttyO1",baudrate=115200,timeout=1)
ser.close()
ser.open()

ser.write("*00004#")
for x in range(0,3):
    s= ser.readline()
    print(s)

