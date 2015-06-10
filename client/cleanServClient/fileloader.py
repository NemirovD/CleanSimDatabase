def loadFiles(datadict):
	if datadict['inputfiles'] is not None:
		datadict['inputfiles'] = [getData(f) for f in datadict['inputfiles']]
	if datadict['outputfiles'] is not None:
		datadict['outputfiles'] = [getData(f) for f in datadict['outputfiles']]
	return datadict

def getData(filename):
	f = {}
	try :
		with open(filename, 'r') as myfile:
			f = {'filename':filename, 'data': myfile.read()}
		return f
	except Exception, e:
		print "Could not open file specified in config: " + filename
		print e
		exit(0)