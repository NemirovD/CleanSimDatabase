import json
import socket
import strings
import dbHandler
from OpenSSL import SSL
from threading import Thread
from traceback import print_exc
from argparse import ArgumentParser 
from sockUtils import sendMessage, recvMessage

class WorkerThread(Thread):
	def __init__(self, conn):
		Thread.__init__(self)
		self.conn = conn

	def run(self):
		message = recvMessage(self.conn)
		datadict = json.loads(message)
		parse(datadict, self.conn)

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
		elif mType == 'CHANGEPASS':
			dbHandler.changepass(datadict, conn)
		else:
			res = {
				'type' : 'textresponse',
				'message' : 'Invalid Message Type: '+mType
			}
			sendMessage(conn, json.dumps(res))
	else:
		res = {
			'type' : 'textresponse',
			'message' : 'Could Not authenticate User',
			'noauth' : 0
		}
		sendMessage(conn, json.dumps(res))

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

			worker = WorkerThread(conn)
			worker.run()

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