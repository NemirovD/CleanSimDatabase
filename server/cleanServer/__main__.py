import json
import socket
import strings
import dbHandler
from sockUtils import sendMessage, recvMessage
from traceback import print_exc
from OpenSSL import SSL
from argparse import ArgumentParser 

def parse(datadict, conn):
	mType = datadict['MessageType']
	if mType == 'REGISTER':
		dbHandler.registerUser(datadict, conn)
		return

	if dbHandler.authenticateUser(datadict):
		if mType == 'ADD':
			dbHandler.addSimulation(datadict, conn)
		elif mType == 'SEARCH':
			dbHandler.searchSimulations(datadict, conn)
		elif mType == 'GRAB':
			dbHandler.grabFile(datadict, conn)
		elif mType == 'GRABALL':
			dbHandler.grabAllFiles(datadict, conn)
		else:
			res = {
				'type' : 'textresponse',
				'message' : 'Invalid Message Type: '+mType
			}
			conn.sendall(json.dumps(res))
	else:
		res = {
			'type' : 'textresponse',
			'message' : 'Could Not authenticate User'
		}
		conn.sendall(json.dumps(res))

def enactArgs():
	p = ArgumentParser(description=strings.programDescription)
	p.add_argument('-i','--init', help=strings.initHelp, action='store_true')
	args = p.parse_args()

	if args.init:
		dbHandler.clean()
	dbHandler.setup()

def main():
	enactArgs()

	context = SSL.Context(SSL.SSLv23_METHOD)
	context.use_privatekey_file('key')
	context.use_certificate_file('cert')

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock = SSL.Connection(context, sock)
	sock.bind(('', 9999))
	sock.listen(1)
	conn = None

	while True:
		try:
			print "Waiting for connection"
			conn, addr = sock.accept()
			message = recvMessage(conn)

			datadict = json.loads(message)
			parse(datadict, conn)

			if conn != None:
				conn.close()

		except KeyboardInterrupt:
			sock.close()
			print "exiting"
			break

		except Exception, e:
			print_exc()
			sock.close()
			break


if __name__ == '__main__':
	main()