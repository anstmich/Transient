class OneVector:

	def __init__(self):
		self.data = []
		self.dlen = 0

	def clear_data(self):
		del self.data[:]
		self.dlen = 0

	def append_value(self, datum):
		self.data.append(datum)
		self.dlen+=1

	def append_multiple(self, data):
		for d in data:
			self.data.append(d)
			self.dlen += 1

class TwoVector:

	def __init__(self):
		self.x = []
		self.y = []

		self.dlenx = 0
		self.dleny = 0

	def clear_data(self):
		del self.x[:]
		self.dlenx = 0
		del self.y[:]
		self.dleny = 0

	def append_value(self, d1, d2):
		self.x.append(d1)
		self.y.append(d2)
		self.dlenx += 1
		self.dleny += 1

	def append_multiple(self, d1, d2):
		if(len(d1) is not len(d2)):
			raise Exception('Input vectors do not have matching length.')

		if(len(d1) == 0):
			raise Warning('Empty input.')
			return

		for v1, v2 in zip(d1, d2):
			self.x.append(v1)
			self.y.append(v2)

			self.dlenx += 1
			self.dleny += 1

