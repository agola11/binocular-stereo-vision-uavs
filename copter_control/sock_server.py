'''
sock_server.py:
	Copter controller FSM for formation flying.

Author:
	Ankush Gola
'''
import socket, time, json

PORT = 6060
BUF_SIZE = 4096

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('localhost', PORT))
ss.listen(2) # listen for 2 connections

c1, c2 = None, None
a1, a2 = None, None
state = 0

def error(ss, msg):
	"""
	for debugging
	"""
	print('ERR: ' + msg)

def print_msgs(msg1, msg2):
	"""
	for debugging
	"""
	global a1, a2
	print a1, ' >> ', msg1
	print a2, ' >> ', msg2

def start():
	"""
	Handle the starting state
	establish a connection between the two clients
	"""
	global c1, c2
	global a1, a2
	global state

	c1, a1 = ss.accept()
	c2, a2 = ss.accept()
	state += 1

def arm_first():
	"""
	Handle the single arm state
	arm the first copter
	"""
	global c1, c2
	global a1, a2
	global BUF_SIZE
	global state

	msg1 = c1.recv(BUF_SIZE)
	msg2 = c2.recv(BUF_SIZE)
	print_msgs(msg1, msg2) # wait for connected messages

	if msg1 != 'Connected' or msg2 != 'Connected':
		state = 9 # exit failure
	else:
		new_msg = 'ARM'
		c1.send(new_msg)
		state += 1

def takeoff_first():
	"""
	Handle the single takeoff state.
	takeoff the first copter.
	"""
	global c1
	global a1
	global BUF_SIZE
	global state

	msg = c1.recv(BUF_SIZE) # wait for the armed message
	print a1, ' >> ', msg
	if msg != 'Armed'
		state = 9 # exit failure
	else:
		new_msg = 'TAKEOFF'
		c1.send(new_msg)
		state += 1
	

def goto_first():
	"""
	Handle the first goto waypoint state.
	"""
	global c1
	global a1
	global BUF_SIZE
	global state

	msg = c1.recv(BUF_SIZE) # wait for taken off message
	print a1, ' >> ', msg1
	if msg != 'Taken Off'
		state = 9 # exit failure
	else:
		new_msg = 'GOTO'
		c1.send(new_msg)
		state += 1

def arm_second():
	"""
	Handle the second armed state
	arm the second copter
	"""
	global c1, c2
	global a1, a2
	global BUF_SIZE
	global state

	msg1 = c1.recv(BUF_SIZE) # wait for the arrival message from first copter
	print a1, ' >> ', msg1
	if msg1 != 'Arrived':
		state = 9 # exit failure
	else:
		new_msg = 'TAKEOFF'
		c2.send(new_msg)
		state += 1

def takeoff_second():
	"""
	Handle the single takeoff state.
	takeoff the first copter.
	"""
	global c2
	global a2
	global BUF_SIZE
	global state

	msg = c2.recv(BUF_SIZE) # wait for the armed message
	print a2, ' >> ', msg
	if msg != 'Armed'
		state = 9 # exit failure
	else:
		new_msg = 'TAKEOFF'
		c2.send(new_msg)
		state += 1

def goto_second():
	global c2
	global a2
	global BUF_SIZE
	global state

	msg = c2.recv(BUF_SIZE) # wait for the armed message
	print a2, ' >> ', msg
	if msg != 'Armed'
		state = 9 # exit failure
	else:
		new_msg = 'TAKEOFF'
		c2.send(new_msg)
		state += 1

def formation():
	pass

def exit_success():
	global state
	state += 1 # increment state to 10

def exit_failure():
	global state
	state += 1 # increment state to 10

states = {0 : start, 1 : arm_first, 2 : takeoff_first, 3 : goto_first, 4 : arm_second, 5 : takeoff_second, 6 : goto_second, 7 : formation, 8 : exit_success, 9 : exit_failure}

# propogate FSM
while state < len(states):
	state = states[state]()

ss.close()