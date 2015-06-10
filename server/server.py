import sys
import json
import peewee
import socket
import MySQLdb
import datetime
import hashlib
import traceback

db = peewee.MySQLDatabase('cleanServ', user='cleanServer', passwd='pass')

#Base Tables
#Provides information about each of the items
class BaseModel(peewee.Model):
	class Meta:
		database = db

class Simulation(BaseModel):
	id = peewee.PrimaryKeyField()
	description = peewee.TextField()
	date = peewee.DateTimeField(default=datetime.datetime.now())

class File(BaseModel):
	id = peewee.PrimaryKeyField()
	name = peewee.CharField()
	path = peewee.CharField(unique=True)

class User(BaseModel):
	id = peewee.PrimaryKeyField()
	uname = peewee.CharField(unique=True)
	pword = peewee.CharField(null=True)

class Keyword(BaseModel):
	id = peewee.PrimaryKeyField()
	keyword = peewee.CharField(unique=True)

class Molecule(BaseModel):
	id = peewee.PrimaryKeyField()
	#I don't know what else to put in here yet
	#There should be an existing list of molecules maybe

#Relational tables
#Relates each of the tables to each other
class FileSimInfo(BaseModel):
	sid = peewee.ForeignKeyField(Simulation, to_field="id")
	fid = peewee.ForeignKeyField(File, to_field="id")

class UserSimInfo(BaseModel):
	sid = peewee.ForeignKeyField(Simulation, to_field="id")
	uid = peewee.ForeignKeyField(User, to_field="id")

class KeywordSimInfo(BaseModel):
	sid = peewee.ForeignKeyField(Simulation, to_field="id")
	kid = peewee.ForeignKeyField(Keyword, to_field="id")

def clean():
	FileSimInfo.drop_table()
	UserSimInfo.drop_table()
	KeywordSimInfo.drop_table()
	Simulation.drop_table()
	File.drop_table()
	User.drop_table()
	Keyword.drop_table()
	Molecule.drop_table()

def setup():
	Simulation.create_table()
	File.create_table()
	User.create_table()
	Keyword.create_table()
	Molecule.create_table()
	FileSimInfo.create_table()
	UserSimInfo.create_table()
	KeywordSimInfo.create_table()



def add(datadict, conn):
	descr = datadict['Description'][0]
	sim = Simulation(description=descr)
	sim.save()

	sim = Simulation.select(Simulation.id).order_by(Simulation.id.desc()).get()
	for keyword in datadict['Keywords']:
		if not Keyword.select(Keyword.id).where(Keyword.keyword == keyword).exists():
			word = Keyword(keyword=keyword)
			word.save()
		kword = Keyword.select(Keyword.id).where(Keyword.keyword == keyword).get()
		ksinfo = KeywordSimInfo(sid=sim.id, kid=kword.id)		
		ksinfo.save()

	for uname in datadict['Name']:
		if not User.select().where(User.uname == uname).exists():
			name = User(uname=uname)
			name.save()
		nam = User.select().where(User.uname == uname).get()
		usinfo = UserSimInfo(sid=sim.id, uid=nam.id)
		usinfo.save()

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

	result = {}
	result['type'] = 'textresponse'
	result['message'] = 'Added Successfully'
	conn.sendall(json.dumps(result))

def search(datadict, conn):
	#the data dict should probably only contain a query
	query = 0
	if datadict['Keywords'] == None:
		query = Simulation.select(Simulation.id).\
					join(UserSimInfo).\
					join(User).\
					where(User.uname << datadict['Name']).\
					distinct().naive()
	elif datadict['Name'] == None:
		query = Simulation.select(Simulation.id).\
					join(KeywordSimInfo).\
					join(Keyword).\
					where(Keyword.keyword << datadict['Keywords']).\
					distinct().naive()
	elif len(datadict['Keywords']) > 0 and len(datadict['Name']) > 0:
		query = Simulation.select(Simulation.id).\
					join(KeywordSimInfo).\
					join(Keyword).\
					where(Keyword.keyword << datadict['Keywords']).\
					switch(Simulation).\
					join(UserSimInfo).\
					join(User).\
					where(User.uname << datadict['Name']).\
					distinct().naive()

	results = {}
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

	results['type'] = 'rows'
	results['data'] = rows
	conn.sendall(json.dumps(results))
		
		# val.id, val.uname, val.description, val.date

	return

def grab(datadict):
	return

def register(datadict):
	return

def parse(datadict, conn):
	mType = datadict['MessageType']
	if mType == 'ADD':
		add(datadict, conn)
	elif mType == 'SEARCH':
		search(datadict, conn)
	elif mType == 'GRAB':
		grab(datadict)
	elif mType == 'REGISTER':
		register(datadict)
	else:
		res = {
			'type' : 'textresponse',
			'message' : 'Invalid Message Type: '+mType
		}
		conn.sendall(json.dumps(res))

def init(init):
	if init == 1:
		clean()
		setup()

def main():
	init(0)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('localhost', 9999))
	sock.listen(1)
	conn = None

	while True:
		try:
			print "Waiting for connection"
			conn, addr = sock.accept()
			datadict = json.loads(conn.recv(4096))
			parse(datadict, conn)

		except KeyboardInterrupt:
			sock.close()
			if conn != None:
				conn.close()
			print "exiting"
			break

		except Exception, e:
			traceback.print_exc()
			sock.close()
			break


		finally:
			if conn != None:
				conn.close()

if __name__ == "__main__":
	main()
		
