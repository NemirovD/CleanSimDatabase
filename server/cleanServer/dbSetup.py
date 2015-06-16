import peewee
import MySQLdb
import datetime

db = peewee.MySQLDatabase('cleanServ', user='cleanServer', passwd='pass')

#Base Models for tables to avoid annoying excess code
class BaseModel(peewee.Model):
	class Meta:
		database = db

#Base Tables
#Provides information about each of the items
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
	pword = peewee.CharField()
	salt = peewee.CharField()

class Keyword(BaseModel):
	id = peewee.PrimaryKeyField()
	keyword = peewee.CharField(unique=True)

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