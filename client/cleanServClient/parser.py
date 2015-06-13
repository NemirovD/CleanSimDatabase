import re
import textwrap

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

prefix = "Description: "
wrapper = textwrap.TextWrapper(initial_indent=prefix, width=70,
                               subsequent_indent=' '*len(prefix))

def prettyPrintResponse(res):
	for row in res['data']:
		print "Names:",
		for name in row['users']:
			print name,

		print "| Date:", row['date']

		print wrapper.fill(row['description'])

		print "Keywords:",
		print ", ".join(row['keywords'])
		print ""

def parseResponse(res):
	if res['type'] == 'rows':
		prettyPrintResponse(res)
	elif res['type'] == 'textresponse':
		print res['message']