import parser
from getpass import getpass
from fileloader import loadSecret

def badArgs(parser):
	print "Incorrect Arguments"
	parser.print_help()
	exit(0)

def getLogin():
	return {
		'User' : raw_input("Username: "),
		'Pass' : getpass('Enter Your Password: ')
	}
	

def enact(command, command_arg,parser):
	datadict = getLogin()

	command = str(command).upper()
	datadict['MessageType'] = command

	if command == 'REGISTER':
		register(datadict)

	elif command == 'CHANGEPASS':
		changepass(datadict)

	elif command == 'ADD' or command == 'SEARCH':
		if not command_arg:
			badArgs(parser)
		datadict.update(updateUsingConfig(command_arg))

	elif command == 'GRAB':
		if not command_arg:
			badArgs(parser)
		datadict.update(grab(command_arg))

	elif command == 'GRABALL':
		if not command_arg:
			badArgs(parser)
		datadict.update(graball(command_arg))

	else:
		badArgs(parser)

	return datadict

def register(datadict):
	cpass = getpass('Confirm The Password: ')
	datadict['Secret'] = loadSecret()

	if cpass != datadict['Pass']:
		print "Passwords do not Match"
		exit(0)

def changepass(datadict):
	pass1 = getpass('Enter a New Password: ')
	pass2 = getpass('Confirm The Password: ')

	if pass1 != pass2:
		print "Passwords do not Match"
		exit(0)
	datadict['nPass'] = pass1

def updateUsingConfig(configFileName):
	return parser.parseConfig(configFileName)

def grab(command_arg):
	return {'fileid' : int(command_arg)}

def graball(command_arg):
	return {'simid' : int(command_arg)}