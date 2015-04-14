'''
sock_client.py:
	Simulated Quadcopter Client

Author:
	Ankush Gola
'''

import time, socket

PORT = 6060
BUF_SIZE = 4096
TIMEOUT = 10

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(('localhost', PORT))
cs.send('Connected')

def error(cs, msg):
	cs.send('ERR: ' + msg)
	cs.close()

#-----------------------------------------------------------

# Expecting "ARM" message
msg = cs.recv(BUF_SIZE)
print msg

if msg == 'ARM':
	# Arm
	print 'ATTEMPTING TO ARM'
	time.sleep(2) # replace with actual arming logic

	# insert spin lock here
	cs.send('ARMED')

	# insert timeout 
	# error(cs, 'TIMEOUT')
else:
	error(cs, 'WRONG MESSAGE')

#-----------------------------------------------------------

# Expecting "TAKE OFF"
msg = cs.recv(BUF_SIZE)
print msg

if msg == 'TAKEOFF':
	# Arm
	print 'ATTEMPTING TO TAKE OFF'
	time.sleep(2) # replace with actual arming logic

	# insert spin lock here
	cs.send('TAKEN OFF')

	# insert timeout 
	# error(cs, 'TIMEOUT')
else:
	error(cs, 'WRONG MESSAGE')

#-----------------------------------------------------------

cs.close()