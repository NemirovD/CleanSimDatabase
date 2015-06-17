def sendMessage(sock, message):
	sock.sendall(bytes(long(len(message))))
	sock.sendall(message)

def recvMessage(conn):
	datalength = long(bytes(conn.recv(4096)))
	message = ""
	for i in range(0, datalength, 4096):
		message += conn.recv(4096)
	return message