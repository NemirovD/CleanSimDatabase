import sys
import json
import peewee
import socket
import MySQLdb
import datetime
import hashlib

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

def init(init):
	if init == 1:
		clean()
		setup()

def add(datadict):
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

def search(datadict):
	#the data dict should probably only contain a query
	return

def parse(datadict):
	mType = datadict['MessageType'][0]
	if mType == 'ADD':
		add(datadict)
	elif mType == 'SEARCH':
		search(datadict)
	else:
		return

def main():
	init(1)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('localhost', 9999))
	sock.listen(1)
	conn = None

	while True:
		try:
			print "Waiting for connection"
			conn, addr = sock.accept()
			datadict = json.loads(conn.recv(4096))
			parse(datadict)

		except KeyboardInterrupt:
			if conn != None:
				conn.close()
			sock.close()
			print ""
			break

		except Exception, e:
			print 'Unexpected error:', str(e)

		finally:
			if conn != None:
				conn.close()

if __name__ == "__main__":
	main()
		
