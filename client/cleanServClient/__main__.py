from parser import parseResponse, parseFile
from fileloader import loadFiles
from samplegenerator import writeSample
import json
import socket
import argparse

parser = argparse.ArgumentParser(description="This is a program to upload simulation information to the CLEAN Database")
parser.add_argument("command", help="The command to send to the database. Options are REGISTER, SEARCH, GRAB and ADD. Ignored only if -s is set.", nargs='?',default=False)
parser.add_argument("configfile", help="The configfile that contains information to send to the database. Ignored only if -s is set.",nargs='?',default=False)
parser.add_argument("-s","--sample-output", help="Writes a sample output file to stdout. This command makes the program ignore position arguments", action="store_true")
args = parser.parse_args()

if args.sample_output:
	writeSample()
	exit(0)

if not (args.configfile or args.command):
	print "Incorrect Arguments"
	parser.print_help()
	exit(0)


saddr = ('localhost', 9999)

#parse and load data
datadict = parseFile(args.configfile)
datadict = loadFiles(datadict)
datadict['MessageType'] = str(args.command).upper()

#json data for sending
message = json.dumps(datadict)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(saddr)
try:
	sock.sendall(message)
	test = sock.recv(4096)
	parseResponse(json.loads(test))
		
except ValueError, e:
	print str(e)
finally:
	sock.close()