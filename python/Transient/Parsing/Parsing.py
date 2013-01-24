from ParsingBackend import AsciiParser, DataTypes
import re

def to_data_type(string):
	string = string.upper()

	if(string == 'NUMBER'):
		return int(DataTypes.DOUBLE) # for simplicity, we prefer doubles
	elif(string == 'DOUBLE'):
		return int(DataTypes.DOUBLE)
	elif(string == 'UCHAR'):
		return int(DataTypes.UCHAR)
	elif(string == 'CHAR'):
		return int(DataTypes.CHAR)
	elif(string == 'STRING'):
		return int(DataTypes.STRING)
	else:
		raise Exception('Data type \'%s\' currently not implemented.' % (string))

class AsciiFormat:

	NONE_FLAG = 'NONE'
	ASSIGNMENT = '='
	START_FLAG = 'START'
	END_FLAG = 'END'

	def __init__(self, format):

		self.format = format
		self.parser = AsciiParser()

		# separate the parse format into discrete pieces
		tokens = re.findall('<(.*?)>', format, re.DOTALL)
		delimiters = re.findall('>(.*?)<', format)

		i = 0

		if(len(tokens) < 2):
			raise Exception('Error: Not enough format tokens in string \'%s\'' % (format))

		tok = tokens[i].split(AsciiFormat.ASSIGNMENT)

		if(tok[0] != AsciiFormat.START_FLAG):
			raise Exception('Invalid Format: Start sequence is ambiguous.  If there is no start byte, specify this with <START=NONE> at the beginning of the format string.')

		# store the start sequence
		self.start_seq = None
		if(tok[1] != AsciiFormat.NONE_FLAG):
			self.start_seq = tok[1]

		i += 1
		tok = tokens[i].split(AsciiFormat.ASSIGNMENT)
		while(tok[0] != AsciiFormat.END_FLAG):
			if(i >= len(tokens)):
				raise Exception('End sequence not found in string %s.' %(format))

			delim = delimiters[i]
			self.parser.add_token(to_data_type(tok[1]), tok[0], delim)

			i += 1
			tok = tokens[i].split(AsciiFormat.ASSIGNMENT)

		# parse end sequence
		self.end_seq = tok[1]

