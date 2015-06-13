import re
import textwrap

def parseFile(filename):
	datadict = {}
	f = open(filename, 'r')
	dtype = None

	tlist = []
	for line in f:
		# print line
		# print re.match('#+.*',line), 'comment'
		# print re.match('[^#\s]\S+',line), 'datatype'
		# print re.match('[ \t]+',line), 'value'
		# print re.match('\s*', line), 'empty'
		if re.match('#+.*',line):
			# print "COMMENT", line[:-1]
			continue

		elif re.match('[^#\s]\S+',line):
			# print "DATATYPE", line[:-1]
			if dtype != None:
				if len(tlist) == 0:
					datadict[dtype] = None
				else:
					datadict[dtype] = tlist
				tlist = []
			dtype = line[:-1]

		elif re.match('[ \t]+',line):
			# print "VALUE", line[:-1]
			tlist.append(line.lstrip()[:-1])

		elif re.match('\s*', line):
			# print "EMPTY", line[:-1]
			continue
			

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