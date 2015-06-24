import sys, tempfile, os
import parser
import strings
from subprocess import call
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
				configString = command_arg.run()
				configString = getDescriptionFromUser(configString)
				datadict.update(updateUsingModule(configString))
				
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

def getDescriptionFromUser(configString):
	import os
	newConfString = ""
	EDITOR = os.environ.get('editor') if os.environ.get('editor') else 'nano'
	with tempfile.NamedTemporaryFile(suffix=".tmp") as tmp:
		tmp.write(strings.addEditorTutorial)
		tmp.write(configString)
		tmp.flush()
		call([EDITOR, tmp.name])
		tmp.seek(0)
		newConfString = tmp.read()
	return newConfString


def updateUsingConfig(configFileName):
	return parser.parseConfig(configFileName, False)

def updateUsingModule(inputstring):
	return parser.parseConfig(inputstring, True)

def grab(command_arg):
	return {'fileid' : int(command_arg)}

def graball(command_arg):
	return {'simid' : int(command_arg)}