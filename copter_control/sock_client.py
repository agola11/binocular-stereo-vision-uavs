import time, socket
from copter_control import CopterControl

# DroneAPI APIConnection
api = local_connect()
cc = CopterControl(api)

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 6060))
clientsocket.send('connected')

msg = clientsocket.recv(1024)
print msg

# Arm
print 'ATTEMPTING TO ARM'

cc.arm()
cc.set_mode('GUIDED')

while not cc.is_armed() and cc.get_mode_name() != 'GUIDED':
	time.sleep(0.5)

clientsocket.send('ARMED')

msg = clientsocket.recv(1024)
print msg

# Takeoff
cc.takeoff(15)

time.sleep(5)

print "MODE: " #+ cc.get_mode_name()

clientsocket.send('TAKEN OFF')

clientsocket.close()