import ssl
import json
import socket
import strings
import commands
import argparse
from sockUtils import sendMessage, recvMessage
from getpass import getpass
from fileloader import loadFiles, loadSecret
from parser import parseResponse, parseFile

parser = argparse.ArgumentParser(description=strings.description)
parser.add_argument("command", help=strings.commandhelp, nargs='?',default=False)
parser.add_argument("command_arg", help=strings.commandarghelp,nargs='?',default=False)
parser.add_argument("-s","--sample-output", help=strings.samplehelp, action="store_true")
parser.add_argument("-u","--user", help=strings.userhelp,nargs='?', default=False)

args = parser.parse_args()

if args.sample_output:
	print strings.samplefile
	exit(0)

if not args.command:
	commands.badArgs(parser)

datadict = commands.enact(args.command, args.command_arg, parser)

#json data for sending
message = json.dumps(datadict)

saddr = ('localhost', 9999)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = ssl.wrap_socket(sock)
sock.connect(saddr)
try:
	sendMessage(sock, message)

	res = recvMessage(sock)
	parseResponse(json.loads(res))
		
except ValueError, e:
	print str(e)
finally:
	sock.close()