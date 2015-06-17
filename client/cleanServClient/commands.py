import parser
from getpass import getpass
from fileloader import loadSecret

def badArgs(parser):
	print "Incorrect Arguments"
	parser.print_help()
	exit(0)

def getLogin():
	uname = raw_input("Username: ")
	upass = getpass('Enter a Password: ')
	return uname, upass

def enact(command, command_arg,parser):
	datadict = {}
	datadict['User'], datadict['Pass'] = getLogin()

	command = str(command).upper()
	datadict['MessageType'] = command

	if command == 'REGISTER':
		register(datadict)

	elif command == 'ADD' or command == 'SEARCH':
		if not (command and command_arg):
			badArgs()
		datadict.update(updateUsingConfig(command_arg))

	elif command == 'GRAB':
		if not (command and command_arg):
			badArgs()
		datadict.update(grab(command_arg))

	return datadict

def register(datadict):
	cpass = getpass('Confirm Password: ')
	datadict['Secret'] = loadSecret()

	if cpass != datadict['Pass']:
		print "Passwords do not Match"
		exit(0)

	return datadict

def updateUsingConfig(configFileName):
	return parser.parseConfig(configFileName)

def grab(command_arg):
	return {'fileid' : int(command_arg)}