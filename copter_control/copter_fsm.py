import zmq
import sys

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock_1 = context.socket(zmq.REP)
sock_1.bind("tcp://127.0.0.1:5660")

sock_2 = context.socket(zmq.REP)
sock_2.bind("tcp://127.0.0.1:5678")

# Get the "Connected" Messages
message = sock_1.recv()
print message
message = sock_2.recv()
print message

# Send the "OKAY TO ARM" message
new = "ARM"
sock_1.send("Server: " + new)
sock_2.send("Server: " + new)


# Get the "Armed" Messages
message = sock_1.recv()
print message
message = sock_2.recv()
print message

# Send the "OKAY TO TAKEOFF" message
new = "OK TO TAKEOFF"
sock_1.send("Server: " + new)
sock_2.send("Server: " + new)
