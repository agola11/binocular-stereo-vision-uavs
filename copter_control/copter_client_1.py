'''
copter_client.py:
	Client program that sends messages to an X8

Author:
	Ankush Gola
'''

import time, zmq
from copter_control import CopterControl

# DroneAPI APIConnection
api = local_connect()
cc = CopterControl(api)

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:5678")

# Send the "Connected" message
new = "Connected"
sock.send("Client1: " + new)

# Wait for OKAY TO ARM
message = sock.recv()
cc.arm()

# spin
while not cc.is_armed() and not api.exit:
	time.sleep(1)

new = "Armed"
sock.send("Client1: " + new)

# Wait for OKAY TO TAKEOFF
message = sock.recv()
print message
cc.set_mode("GUIDED")
time.sleep(4) 
cc.takeoff(15)