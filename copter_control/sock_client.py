'''
sock_client.py:
	Simulated Quadcopter Client

Author:
	Ankush Gola
'''

import time, socket

PORT = 6060
BUF_SIZE = 4096
TIMEOUT = 20 # timeout in seconds

state = 0
cs = None

def print_srv(msg):
	"""
	Print message from the server
	"""
	print "Server:", " >> ", msg

def connect():
	"""
	Handle the connect state.
	Establish a connection with the server
	"""
	global cs

	cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cs.connect(('localhost', PORT))
	cs.send('Connected')
	state += 1

def arm():
	"""
	Handle the arm state.
	Arm the copter.
	"""
	global cs

	msg = cs.recv(BUF_SIZE) # wait for armed message
	
	# cc.arm()
	# cc.set_mode('GUIDED')
	# Insert while loop with timeout here

	time.sleep(4)
	cs.send('Armed')

def takeoff():
	global cs

	msg = cs.recv(BUF_SIZE) # wait for armed message
	
	# cc.takeoff(json.loads(msg)['alt'])
	# Insert while loop with timeout here

	time.sleep(4)
	cs.send('Taken Off')




states = {0 : connect, 1 : arm, 2 : takeoff, 3 : goto_init, 4 : formation, 5 : exit_success, 6 : exit_failure}

# propogate FSM
while state < len(states):
	state = states[state]()

cs.close()