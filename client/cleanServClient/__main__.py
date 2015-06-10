import parser
import fileloader
import json
import textwrap
import socket

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

prefix = "Description: "
wrapper = textwrap.TextWrapper(initial_indent=prefix, width=70,
                               subsequent_indent=' '*len(prefix))

saddr = ('localhost', 9999)

#parse and load data
datadict = parser.parseFile('configSchema.txt')
datadict = fileloader.loadFiles(datadict)

#json data for sending
message = json.dumps(datadict, -1)

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