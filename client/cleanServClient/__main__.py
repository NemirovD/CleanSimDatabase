import ssl
import json
import socket
import argparse
from getpass import getpass
from fileloader import loadFiles
from samplegenerator import writeSample
from parser import parseResponse, parseFile

parser = argparse.ArgumentParser(description="This is a program to upload simulation information to the CLEAN Database")
parser.add_argument("command", help="The command to send to the database. Options are REGISTER, SEARCH, GRAB and ADD. Ignored only if -s is set.", nargs='?',default=False)
parser.add_argument("configfile", help="The configfile that contains information to send to the database. Ignored only if -s is set.",nargs='?',default=False)
parser.add_argument("-s","--sample-output", help="Writes a sample output file to stdout. This command makes the program ignore positional arguments.", action="store_true")
parser.add_argument("-u","--user", help="Specifies the User that will be uploading the server data. If no user specified the user will be prompted.",nargs='?', default=False)

args = parser.parse_args()

if args.sample_output:
	writeSample()
	exit(0)

mType = str(args.command).upper()

if not (args.configfile and args.command) and not mType == 'REGISTER':
	print "Incorrect Arguments"
	parser.print_help()
	exit(0)

uname = args.user
if not uname:
	uname = raw_input("Username: ")
pword = getpass()

datadict = {}
if mType != 'REGISTER':
	#parse and load data
	datadict = parseFile(args.configfile)
	datadict = loadFiles(datadict)
datadict['User'] = uname
datadict['Pass'] = pword
datadict['MessageType'] = mType

#json data for sending
message = json.dumps(datadict)

saddr = ('localhost', 9999)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = ssl.wrap_socket(sock)
sock.connect(saddr)
try:
	sock.sendall(message)
	print sock.cipher()
	test = sock.recv(4096)
	parseResponse(json.loads(test))
		
except ValueError, e:
	print str(e)
finally:
	sock.close()