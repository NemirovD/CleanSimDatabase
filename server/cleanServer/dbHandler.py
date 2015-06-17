import os
import json
import hashlib
from dbSetup import *
from sockUtils import sendMessage, recvMessage

def loadSecret():
	try :
		with open('secret','r') as secretfile:
			return secretfile.read()
	except Exception, e:
		print "Could not open file containing secret"
		print e
		exit(0)

__secret = loadSecret()

def clean():
	FileSimInfo.drop_table(True)
	UserSimInfo.drop_table(True)
	KeywordSimInfo.drop_table(True)
	Simulation.drop_table(True)
	File.drop_table(True)
	User.drop_table(True)
	Keyword.drop_table(True)

def setup():
	Simulation.create_table(True)
	File.create_table(True)
	User.create_table(True)
	Keyword.create_table(True)
	FileSimInfo.create_table(True)
	UserSimInfo.create_table(True)
	KeywordSimInfo.create_table(True)


@db.atomic()
def registerUser(datadict, conn):
	res = {'type' : 'textresponse'}
	query = User.select().where(User.uname == datadict['User'])
	if datadict['Secret'] != __secret:
		res['message'] = 'Your secret does not match the server secret'
	elif query.exists():
		#User already exists with that name
		res['message'] = 'User already exists with that name'
	else:
		newUser = User()
		newUser.uname = datadict['User']
		newUser.salt = os.urandom(16).encode('hex')
		p = hashlib.sha1(newUser.salt + datadict['Pass']).hexdigest()
		newUser.pword = p
		newUser.save()
		res['message'] = 'User Registered Successfully'
	sendMessage(conn, json.dumps(res))
	return

def authenticateUser(datadict):
	row = User.select().where(User.uname == datadict['User'])
	if row.exists():
		uname = datadict['User']
		pword = datadict['Pass']
		userRow = row.get()

		possiblePass = hashlib.sha1(userRow.salt + pword).hexdigest()
		if userRow.pword == possiblePass:
			return True
	return False

@db.atomic()
def addSimulation(datadict, conn):
	result = {}
	result['type'] = 'textresponse'

	descr = None
	if 'Description' in datadict \
		and datadict['Description'] \
		and datadict['Description'] != "":
			descr = datadict['Description'][0]
	else: 
		result['message'] = 'A simulation must a description'
		sendMessage(conn, json.dumps(result))
		return

	sim = Simulation(description=descr)
	sim.save()

	sim = Simulation.select(Simulation.id).order_by(Simulation.id.desc()).get()
	if 'Keywords' in datadict and datadict['Keywords']:
		for keyword in datadict['Keywords']:
			if not Keyword.select(Keyword.id).where(Keyword.keyword == keyword).exists():
				word = Keyword(keyword=keyword)
				word.save()
			kword = Keyword.select(Keyword.id).where(Keyword.keyword == keyword).get()
			ksinfo = KeywordSimInfo(sid=sim.id, kid=kword.id)		
			ksinfo.save()

	uname = datadict['User']
	nam = User.select().where(User.uname == uname).get()
	usinfo = UserSimInfo(sid=sim.id, uid=nam.id)
	usinfo.save()

	if 'inputfiles' in datadict and datadict['inputfiles']:
		for f in datadict['inputfiles']:
			filename = f['filename']
			filedata = f['data']
			filepath = 'files/'+str(hashlib.md5(filedata).hexdigest())

			if not File.select().where(File.path == filepath).exists():
				ff = open(filepath, 'w')
				ff.write(filedata)

				fins = File(name=filename, path=filepath)
				fins.save()

			frow = File.select(File.id).where(File.path == filepath).get()

			fsinfo = FileSimInfo(sid=sim.id, fid=frow.id)
			fsinfo.save()

	
	result['message'] = 'Added Successfully'
	sendMessage(conn, json.dumps(result))
	return

def searchSimulations(datadict, conn):
	#the data dict should probably only contain a query
	query = 0
	noKeywords = 'Keywords' not in datadict or datadict['Keywords'] == None
	noUsers = 'Users' not in datadict or datadict['Users'] == None
	if noKeywords and noUsers:
		res = {
			'type' : 'textresponse',
			'message' : 'You need to add Search terms to the config file.'
		}
		sendMessage(conn, json.dumps(res))
		return
	elif noKeywords:
		query = Simulation.select(Simulation.id).\
					join(UserSimInfo).\
					join(User).\
					where(User.uname << datadict['Users']).\
					distinct().naive()
	elif noUsers:
		query = Simulation.select(Simulation.id).\
					join(KeywordSimInfo).\
					join(Keyword).\
					where(Keyword.keyword << datadict['Keywords']).\
					distinct().naive()
	else:
		query = Simulation.select(Simulation.id).\
					join(KeywordSimInfo).\
					join(Keyword).\
					where(Keyword.keyword << datadict['Keywords']).\
					switch(Simulation).\
					join(UserSimInfo).\
					join(User).\
					where(User.uname << datadict['Users']).\
					distinct().naive()

	results = {}
	if query.exists():
		rows = []
		for val in query:
			result = {}
			simres = Simulation.select().where(Simulation.id == val.id).get()
			result['description'] = simres.description
			result['date'] = str(simres.date)
			result['users'] = []
			for res in User.select().\
						join(UserSimInfo).\
						join(Simulation).\
						where(Simulation.id == val.id):
				result['users'].append(res.uname)

			result['keywords'] = []
			for res in Keyword.select().\
						join(KeywordSimInfo).\
						join(Simulation).\
						where(Simulation.id == val.id):
				result['keywords'].append(res.keyword)
			rows.append(result)

			result['files'] = []
			for res in File.select().\
						join(FileSimInfo).\
						join(Simulation).\
						where(Simulation.id == val.id).\
						distinct():
				t = {
					"id": res.id,
					"filename": res.name
				}
				result['files'].append(t)


		results['type'] = 'rows'
		results['data'] = rows
	else:
		results['type'] = 'textresponse'
		results['message'] = 'No Simulations found using search terms'
	sendMessage(conn, json.dumps(results))
	return

def grabFile(datadict, conn):
	response = {}
	if 'fileid' in datadict and datadict['fileid']:
		query = File.select().where(File.id == datadict['fileid'])

	if query.exists():
		val = query.get()
		f = open(val.path, 'r')
		filetext = f.read()

		response['type'] = 'file'
		response['name'] = val.name
		response['data'] = filetext
	else:
		response = {
			'type' : 'textresponse',
			'Message' : 'There are no files with that ID'
		}
	sendMessage(conn, json.dumps(response))
	return