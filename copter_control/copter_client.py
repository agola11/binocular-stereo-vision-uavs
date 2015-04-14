import time, socket
from copter_control import CopterControl

PORT = 6060
BUF_SIZE = 4096

# DroneAPI APIConnection
api = local_connect()
cc = CopterControl(api)

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(('localhost', PORT))
cs.send('connected')

msg = cs.recv(BUF_SIZE)
print msg

# Arm
print 'ATTEMPTING TO ARM'

cc.arm()
cc.set_mode('GUIDED')

while not cc.is_armed() and cc.get_mode_name() != 'GUIDED':
	time.sleep(0.5)

cs.send('ARMED')

msg = cs.recv(BUF_SIZE)
print msg

# Takeoff
cc.takeoff(15)

time.sleep(5)

print "MODE: " #+ cc.get_mode_name()

cs.send('TAKEN OFF')

cs.close()