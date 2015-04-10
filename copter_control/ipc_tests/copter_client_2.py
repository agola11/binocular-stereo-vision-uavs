'''
copter_control.py:
	Client program that sends messages to an X8

Author:
	Ankush Gola
'''

import time, zmq
from copter_control import CopterControl

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:5660")

new = "Connected"
sock.send("Client2: " + new)

message = sock.recv()
print message

time.sleep(2)
new = "Armed"
sock.send("Client2: " + new)

message = sock.recv()
print message

time.sleep(2)
new = "Taken Off"
sock.send("Client2: " + new)

"""
# DroneAPI APIConnection
api = local_connect()
cc = CopterControl(api)

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:5660")

# Send the "Connected" message
new = "Connected"
sock.send("Client2: " + new)

# Wait for OKAY TO ARM
message = sock.recv()
cc.arm()

# spin
while not cc.is_armed() and not api.exit:
	time.sleep(1)

new = "Armed"
sock.send("Client2: " + new)

# Wait for OKAY TO TAKEOFF
message = sock.recv()
print message
cc.set_mode("GUIDED")
time.sleep(4) 
cc.takeoff(15)
"""