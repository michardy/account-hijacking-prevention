# This script compares user data
# it is also called to intialize modules that hash and compare data

import mongo_int

import tornado.ioloop
from tornado import gen

import logging
logger = logging.getLogger(__name__)

class Receiver():
	def __init__(self):
		self.__hashers = {}
		self.__translators = {}
		self.__comparers = {}
		self.__maxscores = {}

	def add_hasher(self, name, fxn): #called on by any data hashing module on startup
		#registers a function to hash a type of data
		self.__hashers[name] = fxn

	def add_translator(self, name, fxn):
		self.__translators[name] = fxn

	def add_comparer(self, name, fxn, score): #called by any data collecting module on startup
		#registers a function to compare hashes of a type of data
		self.__comparers[name] = fxn
		self.__maxscores[name] = score

	@gen.coroutine
	def add_data(self, req, headers, db): #called when data is received
		if req['name'] in self.__comparers.keys():
			hash = yield self.__hashers[req['name']](req['data'],
				req['ck'], headers, db)
			site = yield mongo_int.get_site_by_client_key(req['ck'],
				headers.get("Host"), db)
			yield mongo_int.add_to_session(hash, req['name'],
				req['sessionID'], site, db)
			return(200, 'OK')
		else:
			logger.warning('Could not find a handler for "' + req['name'] + '"')
			return(400, 'Err: Could not find a handler for "' + req['name'] + '"')

	@gen.coroutine
	def copy_data(self, req, db):
		sid = req['sid']
		uid = req['uid']
		site = yield mongo_int.get_site_by_server_key(req['ak'], db)
		session = yield mongo_int.get_session(sid, site, db)
		if session.keys():
			data = {}
			for dt in session.keys():
				data[dt] = self.__translators[dt](session[dt])
			mongo_int.write_user(uid, data, site, db)
			return(200, 'OK')
		else:
			logger.warning ('Client attempted to register user with expired or nonexistent session')
			return(404, 'Invalid Session')

	@gen.coroutine
	def get_trust(self, sid, uid, site, db):
		total = 0
		actmax = 0
		for i in self.__comparers.keys():
			actmax += self.__maxscores[i]
			total += yield self.__comparers[i](sid, uid, site, db)
		try:
			out = (200, str(total/actmax))
		except ZeroDivisionError:
			logger.critical('This server does not have any client data collection and analysis modules installed')
			out = (501, 'This server does not have any data collection and analysis modules installed')
		return(out)
