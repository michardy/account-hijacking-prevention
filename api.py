# This script compares user data
# it is also called to intialize modules that hash and compare data

import mongo_int

import tornado.ioloop
from tornado import gen

class receiver():
	def __init__(self):
		self.__hashers = {}
		self.__translators = {}
		self.__comparers = {}
		self.__maxscores = {}

	def addHasher(self, name, fxn): #called on by any data hashing module on startup
		#registers a function to hash a type of data
		self.__hashers[name] = fxn

	def addTranslator(self, name, fxn):
		self.__translators[name] = fxn

	def addComparer(self, name, fxn, score): #called by any data collecting module on startup
		#registers a function to compare hashes of a type of data
		self.__comparers[name] = fxn
		self.__maxscores[name] = score

	@gen.coroutine
	def addData(self, req, db): #called when data is received
		#TODO: move this fxn out of this class?
		if req['name'] in self.__comparers.keys():
			hash = yield self.__hashers[req['name']](req['data'], req['ck'], 'test', db)
			site = yield mongo_int.getSiteByClientKey(req['ck'], 'test', db)
			yield mongo_int.addToSession(hash, req['name'],
				req['sessionID'], site, db)
			return(200, 'OK')
		else:
			return(400, 'Err: Could not find a handler for "' + req.get_argument('name') + '"')

	@gen.coroutine
	def copyData(self, req, db):
		sid = req['sid']
		uid = req['uid']
		site = yield mongo_int.getSiteByServerKey(req['ak'], db)
		session = yield mongo_int.getSession(sid, site, db)
		print(session)
		user = {'sessionID': sid, 'data':{}}
		for dt in session.keys():
			user['data'][dt] = self.__translators[dt](session[dt])
		print(user)
		mongo_int.writeUser(uid, user, site, db)
		return(200, 'OK')

	@gen.coroutine
	def gTrust(self, sid, uid, site, db):
		total = 0
		actmax = 0
		for i in self.__comparers.keys():
			actmax += self.__maxscores[i]
			total += yield self.__comparers[i](sid, uid, site, db)
		print(total/actmax)
		return(str(total/actmax))
