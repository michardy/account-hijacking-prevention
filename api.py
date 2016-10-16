# This script compares user data
# it is also called to intialize modules that hash and compare data

import logging

class receiver():
	def __init__(self):
		self.__hashers = {}
		self.__comparers = {}
		self.__maxscores = {}

	def addHasher(self, name, fxn): #called on by any data hashing module on startup
		#registers a function to hash a type of data
		self.__hashers[name] = fxn

	def addComparer(self, name, fxn, score): #called by any data collecting module on startup
		#registers a function to compare hashes of a type of data
		self.__comparers = {}
		self.__maxscores[name] = score
		self.__scores[name] = -1

	def addData(self, req): #called when data is received
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

	def gTrust(self, SID, UID, db):
		total = 0
		actmax = 0
		for i in self.__comparers.keys():
			if self.__scores[i] > -1:
				actmax += self.__maxscores[i]
				total += self.__scores[i]
		return(total/actmax)
