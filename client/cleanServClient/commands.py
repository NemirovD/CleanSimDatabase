import parser
from getpass import getpass
from types import ModuleType
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
	

def enact(command, command_arg, parser):
	datadict = {}

	command = str(command).upper()
	datadict['MessageType'] = command

	if not command_arg:
		datadict.update(getLogin())

		if command == 'REGISTER':
			register(datadict)

		elif command == 'CHANGEPASS':
			changepass(datadict)

		else:
			badArgs(parser)

	if command_arg:
		if command == 'ADD' or command == 'SEARCH':
			if type(command_arg) is ModuleType:
				command_arg.run()
				datadict.update(updateUsingConfig("addConfig.txt"))

			else:
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
		datadict.update(getLogin())
	return datadict

def register(datadict):
	cpass = getpass('Confirm The Password: ')
	datadict['Secret'] = loadSecret()

	if cpass != datadict['Pass']:
		print "Passwords do not Match"
		exit(0)
	return datadict

def changepass(datadict):
	pass1 = getpass('Enter a New Password: ')
	pass2 = getpass('Confirm The Password: ')

	if pass1 != pass2:
		print "Passwords do not Match"
		exit(0)
	datadict['nPass'] = pass1
	return datadict

def updateUsingConfig(configFileName):
	return parser.parseConfig(configFileName)

def grab(command_arg):
	return {'fileid' : int(command_arg)}

def graball(command_arg):
	return {'simid' : int(command_arg)}