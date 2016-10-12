import logging

#log = logging.logger

class receiver():
	def __init__(self):#initialize db connection
		self.__hashers = {}
		self.__comparers = {}
		self.__maxscores = {}

	def add_hasher(self, name, fxn): #called on by any data collecting module on startup
		#registers a function to hash a type of data
		self.__hashers[name] = fxn

	def add_comparer(self, name, fxn, score): #called by any data collecting module on startup
		#registers a function to compare hashes of a type of data
		self.__comparers = {}
		self.__maxscores[name] = score
		self.__scores[name] = -1

	def add_data(self, req): #called when data is received
		#TODO: move this fxn out of this class?
		if req.get_argument('name') in self.__comparers.keys():
			request.write('OK')
			'''
			hash = self.hashers[req.get_getargument('name')](req.get_argument('data'))
			save(req.get_argument('sessionID'),
				req.get_argument('name'), hash)
			'''
		else:
			req.write('Err: Could not find a handler for "' + req.get_argument('name') + '"')
			req.set_status(400)

'''	def run(self, request):
		name = request.get_argument('name')
		try:
			scores[name] = self.__fxnList[name](request, self.__username)
			return (0)
		except IndexError:
			print('Client input error: Could not find handler with name of ' + name + '.  ')
			return(1)
'''

	def gTrust(self):
		total = 0
		actmax = 0
		for i in fxnList.keyes():
			if self.__scores[i] > -1:
				actmax += self.__maxscores[i]
				total += self.__scores[i]
		return(total/actmax)
