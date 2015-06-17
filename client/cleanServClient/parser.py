import re
import filewriter
import fileloader
import textwrap

def parseConfig(filename):
	return fileloader.loadFiles(parseFile(filename))

def parseFile(filename):
	datadict = {}
	f = open(filename, 'r')
	dtype = None

	tlist = []
	for line in f:

		if not re.match('#*\s*.+', line):
			# Line is empty
			continue

		elif re.match('#+.*',line):
			# Line is a comment
			continue

		elif re.match('[^#\s]\S+',line):
			# The line specifies a datatype
			if dtype != None:
				if len(tlist) == 0:
					datadict[dtype] = None
				else:
					datadict[dtype] = tlist
				tlist = []
			dtype = line.rstrip()

		elif re.match('[ \t]+.+',line):
			# The line specifies a value for a datatype
			tlist.append(line.lstrip().rstrip('\n'))

	# Needed for the final Datatype
	if len(tlist) == 0:
		datadict[dtype] = None
	else:
		datadict[dtype] = tlist

	return datadict

def createTextWrapper(prefix):
	return textwrap.TextWrapper(initial_indent=prefix,
                               subsequent_indent=' '*len(prefix))

descrwrapper = createTextWrapper("Description: ")

def prettyPrintResponse(res):
	for row in res['data']:
		print "Names:",
		for name in row['users']:
			print name,

		print "| Date:", row['date']

		print descrwrapper.fill(row['description'])

		print "Keywords:",
		print ", ".join(row['keywords'])
		
		pre = "Files: "
		fill = (len(pre)-1)*' '
		print pre
		for i in row['files']:
			print fill, "id -", i['id'], "| filename -", i['filename']
		print ""

def parseResponse(res):
	if res['type'] == 'rows':
		prettyPrintResponse(res)
	elif res['type'] == 'textresponse':
		print res['message']
	elif res['type'] == 'file':
		filewriter.writefile(res['name'],res['data'])
	elif res['type'] == 'multifile':
		for f in res['files']:
			filewriter.writefile(f['name'],f['data'])