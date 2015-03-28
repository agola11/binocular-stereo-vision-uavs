import zmq
import sys

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://127.0.0.1:5678")

# Run a simple "Echo" server
while True:
	message = sock.recv()
	print message

	#new = sys.stdin.readline()
	new = "From Server"
	sock.send("Server: " + new)