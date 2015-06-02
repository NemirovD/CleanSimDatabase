def parseFile(filename):
	datadict = {}
	f = open(filename, 'r')
	dtype = None

	tlist = []
	for line in f:
		if line[0] == '#' or line[0] == '\n':
			#This would be a comment
			continue

		if line[0] == '\t':
			# Value
			tlist.append(line.split('\t')[1].rstrip('\n'))

		else:
			#Data types
			if dtype != None:
				if len(tlist) == 0:
					datadict[dtype] = None
				else:
					datadict[dtype] = tlist
				tlist = []
			dtype = line.rstrip('\n')

	if len(tlist) == 0:
		datadict[dtype] = None
	else:
		datadict[dtype] = tlist

	return datadict