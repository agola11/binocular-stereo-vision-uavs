'''
sock_client.py:
	Simulated Copter Client

Author:
	Ankush Gola
'''

import time, socket, json
import numpy as np

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

	global cs
	global state

	msg = cs.recv(BUF_SIZE) 

	if msg != 'ARM':
		error(msg)
		state = 6 # exit failure
	else:
		# cc.arm()
		# cc.set_mode('GUIDED')
		# Insert while loop with timeout here
		time.sleep(4)
		cs.send('Armed')
		state += 1

def takeoff():
	"""
	Handle the takeoff state.
	Make the copter takeoff
	"""

	print "In the takeoff state"

	global cs
	global state

	msg = json.loads(cs.recv(BUF_SIZE)) # wait for server message
	
	if msg['msg'] != 'TAKEOFF':
		error(msg)
		state = 6 # exit failure
	else:
		# cc.arm()
		# cc.set_mode('GUIDED')
		# cc.takeoff(json.loads(msg)['alt'])
		# Insert while loop with timeout here
		time.sleep(4)
		print 'Taken Off to %d' % msg['arg1']
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

	msg = json.loads(cs.recv(BUF_SIZE)) # wait for server message
	
	if msg['msg'] != 'GOTO':
		error(msg)
		state = 6 # exit failure
	else:
		# cc.arm()
		# cc.set_mode('GUIDED')
		# cc.takeoff(json.loads(msg)['alt'])
		# Insert while loop with timeout here
		time.sleep(4)
		print 'Arrived at ', str(msg['arg1'])
		cs.send('Arrived')
		state += 1

def diag_line((lat0, lon0, alt0), (lat, lon, alt), k=5):
	"""
	return a path for the drone to follow
	"""
	lats = np.linspace(lat0, lat, k)
	lons = np.linspace(lon0, lon, k)
	alts = np.linspace(alt0, alt, k)
	p = zip(lats, lons, alts)
	return p

def formation():
	print "Formation"
	global state

	msg = json.loads(cs.recv(BUF_SIZE))
	if msg['msg'] != 'FORMATION':
		error(msg)
		state = 6
	else:
		print 'Starting at ', str(msg['arg1']), ' Going to ', str(msg['arg2']), ' step of ', msg['arg3']
		ps = diag_line(msg['arg1'], msg['arg2'], msg['arg3'])
		print 'Path = ', ps
		for p in ps[1:]:
			print 'Going to ', p
			time.sleep(1) # replace this with a loop
			print 'Arrived'
			cs.send('Arrived')
			cs.recv(BUF_SIZE)
		cs.send('DONE')
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
TIMEOUT = 20 # timeout in seconds

state = 0
cs = None

states = {0 : connect, 1 : arm, 2 : takeoff, 3 : goto_init, 4 : formation, 5 : exit_success, 6 : exit_failure}

# propogate FSM
while state < len(states):
	states[state]()

cs.close()