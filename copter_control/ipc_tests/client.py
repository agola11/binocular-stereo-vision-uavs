import zmq
import sys

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:5678")


#new = sys.stdin.readline()
new = "From Client"
sock.send("Client: " + new)
print sock.recv()