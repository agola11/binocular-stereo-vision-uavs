'''
sock_server.py:
	Copter controller FSM for formation flying.

Author:
	Ankush Gola
'''
import socket, time, json

def error(msg):
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
		error(msg1)
		error(msg2)
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
	if msg != 'Armed':
		error(msg)
		state = 9 # exit failure
	else:
		new_msg = {}
		new_msg['msg'] = 'TAKEOFF'
		new_msg['arg1'] = init1[2]
		c1.send(json.dumps(new_msg))
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
	print a1, ' >> ', msg
	if msg != 'Taken Off':
		error(msg)
		state = 9 # exit failure
	else:
		new_msg = {}
		new_msg['msg'] = 'GOTO'
		new_msg['arg1'] = init1
		c1.send(json.dumps(new_msg))
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
		error(msg1)
		state = 9 # exit failure
	else:
		new_msg = 'ARM'
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
	if msg != 'Armed':
		error(msg)
		state = 9 # exit failure
	else:
		new_msg = {}
		new_msg['msg'] = 'TAKEOFF'
		new_msg['arg1'] = init2[2]
		c2.send(json.dumps(new_msg))
		state += 1

def goto_second():
	"""
	Handle the goto second state.
	"""
	global c2
	global a2
	global BUF_SIZE
	global state

	msg = c2.recv(BUF_SIZE) # wait for the taken off message
	print a2, ' >> ', msg
	if msg != 'Taken Off':
		error(msg)
		state = 9 # exit failure
	else:
		new_msg = {}
		new_msg['msg'] = 'GOTO'
		new_msg['arg1'] = init2
		c2.send(json.dumps(new_msg))
		state += 1

def formation():
	"""
	Handle the formation state.
	wait for messages at each stage of the path step.
	"""
	global c1, c2
	global a1, a2
	global BUF_SIZE
	global state

	msg = c2.recv(BUF_SIZE) # wait for the arrived message
	print a2, ' >> ', msg
	if msg != 'Arrived':
		error(msg)
		state = 9 # exit failure
	else:
		msg1, msg2 = {}, {}
		msg1['msg'] = 'FORMATION'
		msg2['msg'] = 'FORMATION'
		
		msg1['arg1'] = init1
		msg1['arg2'] = end1
		msg1['arg3'] = step

		msg2['arg1'] = init2
		msg2['arg2'] = end2
		msg2['arg3'] = step

		c1.send(json.dumps(msg1))
		c2.send(json.dumps(msg2))
		while True:
			msg1 = c1.recv(BUF_SIZE)
			msg2 = c2.recv(BUF_SIZE)
			if msg1 == 'DONE' and msg2 == 'DONE':
				break
			elif msg1 != 'Arrived' or msg2 != 'Arrived':
				error(msg1)
				error(msg2)
				state = 9
				return
			else:
				new_msg = 'GO'
				c1.send(new_msg)
				c2.send(new_msg)
		
		state += 1

def exit_success():
	"""
	Handle the exit success state.
	"""
	global state
	print "EXIT SUCCESS"
	state += 2 # increment state to 10

def exit_failure():
	"""
	Handle the exit failure state.
	"""
	global state
	global c1, c2
	global a1, a2

	# Tell clients to close connections
	c1.send("CLOSE")
	c2.send("CLOSE")

	print "EXIT FAILURE"
	state += 1 # increment state to 10

states = {0 : start, 1 : arm_first, 2 : takeoff_first, 3 : goto_first, 4 : arm_second, 5 : takeoff_second, 6 : goto_second, 7 : formation, 8 : exit_success, 9 : exit_failure}

PORT = 6060
BUF_SIZE = 4096

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('localhost', PORT))
ss.listen(2) # listen for 2 connections

c1, c2 = None, None
a1, a2 = None, None
state = 0

init1 = (40.345851, -74.650123, 15) # 40 left
end1 = (40.345969, -74.650181, 30) # 20 left

init2 = (40.345654, -74.650001, 15) # 40 right
end2 = (40.345520, -74.649927, 30) # 20 left

step = 5

# propogate FSM
while state < len(states):
	states[state]()

ss.close()