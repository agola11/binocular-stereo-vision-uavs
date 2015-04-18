'''
sock_client.py:
	Simulated Quadcopter Client

Author:
	Ankush Gola
'''

import time, socket, json
from copter_control import CopterControl

def print_srv(msg):
	"""
	Print message from the server
	"""
	print "Server:", " >> ", msg

def error(msg):
	"""
	for debugging
	"""
	print('ERR: ' + msg)

def connect():
	"""
	Handle the connect state.
	Establish a connection with the server
	"""

	print "In connection state"

	global cs
	global state

	cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cs.connect(('localhost', PORT))
	cs.send('Connected')
	state += 1

def arm():
	"""
	Handle the arm state.
	Arm the copter.
	"""

	print "In arm state"

	global cs, cc
	global state

	msg = cs.recv(BUF_SIZE) 

	if msg != 'ARM':
		error(msg)
		state = 6 # exit failure
	else:
		cc.arm()
		cc.set_mode('GUIDED')

		to = time.time() + TIMEOUT
		while not cc.is_armed() and cc.get_mode_name() != 'GUIDED':
			if time.time() > to:
				cs.send('TIMEOUT')
				state = 6
				return
			time.sleep(0.1)

		cs.send('Armed')
		state += 1

def takeoff():
	"""
	Handle the takeoff state.
	Make the copter takeoff
	"""

	print "In the takeoff state"

	global cs, cc
	global state

	msg = cs.recv(BUF_SIZE) # wait for server message
	
	if msg != 'TAKEOFF':
		error(msg)
		state = 6 # exit failure
	else:
		cc.takeoff(15)
		# cc.set_mode('GUIDED')
		# cc.takeoff(json.loads(msg)['alt'])
		# Insert while loop with timeout here
		time.sleep(4)
		cs.send('Taken Off')
		state += 1

def goto_init():
	"""
	Handle the goto_init state.
	Make the copter go to the first location.
	"""

	print "In the goto_init state"

	global cs
	global state

	msg = cs.recv(BUF_SIZE) # wait for server message
	
	if msg != 'GOTO':
		error(msg)
		state = 6 # exit failure
	else:
		# cc.arm()
		# cc.set_mode('GUIDED')
		# cc.takeoff(json.loads(msg)['alt'])
		# Insert while loop with timeout here
		time.sleep(4)
		cs.send('Arrived')
		state += 1

def formation():
	print "Formation"
	global state

	msg = cs.recv(BUF_SIZE)
	state += 1

def exit_success():
	print "EXIT SUCCESS"

	global state
	state += 2

def exit_failure():
	global cs
	global state

	print "EXIT FAILURE"
	state += 1


PORT = 6060
BUF_SIZE = 4096
TIMEOUT = 30 # timeout in seconds
state = 0 # initial state
cs = None

states = {0 : connect, 1 : arm, 2 : takeoff, 3 : goto_init, 4 : formation, 5 : exit_success, 6 : exit_failure}

# DroneAPI APIConnection
api = local_connect()
cc = CopterControl(api)

# propogate FSM
while state < len(states):
	states[state]()

cs.close()