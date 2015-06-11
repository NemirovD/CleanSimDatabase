import ssl
import json
import socket
import strings
import argparse
from getpass import getpass
from fileloader import loadFiles
from parser import parseResponse, parseFile

parser = argparse.ArgumentParser(description=strings.description)
parser.add_argument("command", help=strings.commandhelp, nargs='?',default=False)
parser.add_argument("configfile", help=strings.configfilehelp,nargs='?',default=False)
parser.add_argument("-s","--sample-output", help=strings.samplehelp, action="store_true")
parser.add_argument("-u","--user", help=strings.userhelp,nargs='?', default=False)

args = parser.parse_args()

if args.sample_output:
	print strings.samplefile
	exit(0)

mType = str(args.command).upper()

if not (args.configfile and args.command) and not mType == 'REGISTER':
	print "Incorrect Arguments"
	parser.print_help()
	exit(0)

uname = args.user
if not uname:
	uname = raw_input("Username: ")
pwor1 = getpass('Enter a Password: ')

if mType == 'REGISTER':
	pwor2 = getpass('Confirm Password: ')
	# secret = raw_input('Enter Shared Secret: ')

if pwor1 != pwor2:
	print "Passwords don't Match"
	exit(0)

datadict = {}
if mType != 'REGISTER':
	#parse and load data
	datadict = parseFile(args.configfile)
	datadict = loadFiles(datadict)
datadict['User'] = uname
datadict['Pass'] = pwor1
# datadict['Secret'] = secret
datadict['MessageType'] = mType


#json data for sending
message = json.dumps(datadict)

saddr = ('localhost', 9999)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = ssl.wrap_socket(sock)
sock.connect(saddr)
try:
	sock.sendall(message)
	test = sock.recv(4096)
	parseResponse(json.loads(test))
		
except ValueError, e:
	print str(e)
finally:
	sock.close()