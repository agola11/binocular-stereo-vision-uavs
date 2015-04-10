import zmq
import sys

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:5677")

#new = sys.stdin.readline()
new = "From Client2"
sock.send("Client2: " + new)
print sock.recv()