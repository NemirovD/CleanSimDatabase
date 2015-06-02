import parser
import fileloader
import json
import socket
saddr = ('localhost', 9999)

#parse and load data
datadict = parser.parseFile('configSchema.txt')
datadict = fileloader.loadFiles(datadict)

#json data for sending
message = json.dumps(datadict, -1)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(saddr)
try:
	sock.sendall(message)
finally:
	sock.close()