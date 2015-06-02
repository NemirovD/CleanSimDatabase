def loadFiles(datadict):
	if datadict['inputfiles'] is not None:
		datadict['inputfiles'] = [getData(f) for f in datadict['inputfiles']]
	if datadict['outputfiles'] is not None:
		datadict['outputfiles'] = [getData(f) for f in datadict['outputfiles']]
	return datadict

def getData(filename):
	f = {}
	with open(filename, 'r') as myfile:
		f = {'filename':filename, 'data': myfile.read()}
	return f