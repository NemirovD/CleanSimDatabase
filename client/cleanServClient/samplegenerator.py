sample = """# Comments begin with a hashtag

# Name of the data type will be untabbed words
# The value of the named data type will be after a tab character

#The General Design is
#DataType
#	Value
#	Another Value

# Datatypes
#	MessageType
#		ADD OR SEARCH
#	Name
#	Description
#	Keywords
#	inputfiles
#	outputfiles

Name
	Taylor

MessageType
	SEARCH

Description
	Let's make this a really really long description so hopefully it'll wrap. This simulation was designed to do very import stuff, as are all simulations that are on this database.

Keywords

inputfiles
	configSchema.txt

outputfiles
"""

def writeSample():
	print sample
