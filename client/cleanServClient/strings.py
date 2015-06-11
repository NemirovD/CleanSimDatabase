description = \
"""
This is a program to upload simulation information to the CLEAN Database.
"""

configfilehelp = \
"""
The configfile that contains information to send to the database.
Ignored if -s is set or if command is REGISTER.
"""

commandhelp = \
"""
The command to send to the database.
Options are REGISTER, SEARCH, GRAB and ADD.
Ignored only if -s is set.
When using the register command no config file is needed.
"""

samplehelp = \
"""
Writes a sample output file to stdout. 
This command makes the program ignore positional arguments 
like command and configfile.
"""

userhelp = \
"""
Specifies the User that will be uploading the server data.
If no user specified the user will be prompted.
"""

samplefile = \
"""
# Comments begin with a hashtag

# The General Design is
# DataType
#	Value
#	Another Value

# Datatypes
#	Users
#	Description
#	Keywords
#	inputfiles
#	outputfiles

# A config file is used when someone wants to add to or search the database
# The relevant fields when searching are:
# 		Users
#		Keywords
# 		Date  		(Date Added) (Uses ISO standard YYYY-MM-DD) (Not Implemented yet)
# The relevant fields when adding are:
#		Description
#		Keywords
#		inputfiles
#		outputfiles

Description
	Let's make this a really really long description so hopefully it'll wrap. This simulation was designed to do very import stuff, as are all simulations that are on this database.

Keywords
	test
	t
	yes

inputfiles
	INCAR

outputfiles
"""