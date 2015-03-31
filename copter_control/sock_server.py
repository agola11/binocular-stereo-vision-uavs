import socket, time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8089))
serversocket.listen(2) # listen for 2 connections

def recv_messages((c1, a1), (c2, a2)):
	msg1 = c1.recv(1024)
	msg2 = c2.recv(1024)

	print a1, ' >> ', msg1
	print a2, ' >> ', msg2

c1, a1 = serversocket.accept()
c2, a2 = serversocket.accept()
print c1, a1
print c2, a2

recv_messages((c1, a1), (c2, a2))

new_msg = 'OKAY TO ARM'
c1.send(new_msg)
c2.send(new_msg)

recv_messages((c1, a1), (c2, a2))

new_msg = 'OKAY TO TAKEOFF'
c1.send(new_msg)
c2.send(new_msg)

recv_messages((c1, a1), (c2, a2))
serversocket.close()