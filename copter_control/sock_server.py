'''
sock_server.py:
	Copter controller FSM for formation flying.

Author:
	Ankush Gola
'''
import socket, time

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
	ss.close()

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

def takeoff_first(c):
	# wait for armed messages
	pass

def goto_first(c):
	pass

def arm_second(c):
	pass

def takeoff_second(c):
	pass

def goto_second(c):
	pass

def formation(c):
	pass

def exit_success(c):
	pass

def exit_failure(c):
	pass

states = {0 : start, 1 : arm_first, 2 : takeoff_first, 3 : goto_first, 4 : arm_second, 5 : takeoff_second, 6 : goto_second, 7 : formation, 8 : exit_success, 9 : exit_failure}

# propogate FSM
while state < len(states):
	state = states[state]()


c1, a1 = ss.accept()
c2, a2 = ss.accept()

recv_messages((c1, a1), (c2, a2))

new_msg = 'ARM'
c1.send(new_msg)
c2.send(new_msg)

recv_messages((c1, a1), (c2, a2))

new_msg = 'TAKEOFF'
c1.send(new_msg)
c2.send(new_msg)

recv_messages((c1, a1), (c2, a2))

ss.close()