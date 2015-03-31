import time
from copter_control import CopterControl
import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8089))
clientsocket.send('connected')

msg = clientsocket.recv(1024)
print msg

time.sleep(2)
clientsocket.send('ARMED')

msg = clientsocket.recv(1024)
print msg

time.sleep(4)
clientsocket.send('TAKEN OFF')

clientsocket.close()