import imp
import os.path
import sys
import ssl
import json
import socket
import strings
import commands
import argparse
from getpass import getpass
from parser import parseResponse, parseFile
from fileloader import loadFiles, loadSecret
from sockUtils import sendMessage, recvMessage



parser = argparse.ArgumentParser(description=strings.description)
parser.add_argument("command", help=strings.commandhelp, nargs='?',default=False)
parser.add_argument("command_arg", help=strings.commandarghelp,nargs='?',default=False)
parser.add_argument("-s","--sample-output", help=strings.samplehelp, action="store_true")
parser.add_argument("-m", "--use-module", help=strings.usemodulehelp, default=False)

args = parser.parse_args()

if args.sample_output:
	print strings.samplefile
	exit(0)

extmodule = None
if args.use_module and os.path.exists(args.use_module):
	base = os.path.basename(args.use_module).split(".")[0]
	extmodule = imp.load_source(base, args.use_module)
	print extmodule
	if extmodule is None:
		print "Could not load module"
		exit(0)


if not args.command:
	commands.badArgs(parser)

if args.use_module:
	datadict = commands.enact(args.command, extmodule, parser, module=True)
else:
	datadict = commands.enact(args.command, args.command_arg, parser)

#json data for sending
message = json.dumps(datadict)

def connect():
	global sock
	saddr = ('localhost', 9999)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock = ssl.wrap_socket(sock)
	sock.connect(saddr)

try:
	connect()
	sendMessage(sock, message)
	res = json.loads(recvMessage(sock))
	while 'noauth' in res:
		print res['message']
		try:
			datadict.update(commands.getLogin())
			message = json.dumps(datadict)
		except KeyboardInterrupt:
			sys.stdout.write("\r")
			exit(0)
		
		connect()
		sendMessage(sock, message)
		res = json.loads(recvMessage(sock))
	parseResponse(res)
		
except ValueError, e:
	print str(e)
finally:
	sock.close()