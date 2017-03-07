# This script compares user data
# it is also called to intialize modules that hash and compare data

import mongo_int

import tornado.ioloop
from tornado import gen

import logging
logger = logging.getLogger(__name__)

class Receiver():
	"""The API request receiver class"""
	def __init__(self):
		self.__hashers = {}
		self.__translators = {}
		self.__comparers = {}
		self.__maxscores = {}

	def add_hasher(self, name, fxn): 
		"""This is called by each module on startup to register its sitewide hasher.  """
		self.__hashers[name] = fxn

	def add_translator(self, name, fxn):
		"""This is called by each module on startup to register its data translator.
		Translators hash data with a per user salt and hash.  
		"""
		self.__translators[name] = fxn

	def add_comparer(self, name, fxn, score):
		"""This is called by each module on startup to register its hash comparer.  """
		self.__comparers[name] = fxn
		self.__maxscores[name] = score

	@gen.coroutine
	def add_data(self, req, headers, db):
		"""This function is called when data is received to store data"""
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
		"""This function is called to store session data permenantly to the user profile"""
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
		"""This scores how trustworth a user is as a number between 1 and zero.  
		The score is based on how much session data matches the data stored in their user profile
		"""
		try:
			user = yield mongo_int.get_user_dat(uid, site, db)
		except TypeError:
			logger.warning('Client attempted to get trust for nonexistant user')
			return(404, "Invalid User")
		try:
			session = yield mongo_int.get_session(sid, site, db)
		except TypeError:
			logger.warning('Client attempted to get trust for expired or non existant session')
			return(404, "Invalid Session")
		total = 0
		actmax = 0
		for i in self.__comparers.keys():
			actmax += self.__maxscores[i]
			total += yield self.__comparers[i](session, user, site, db)
		try:
			return(200, str(total/actmax))
		except ZeroDivisionError:
			logger.critical('This server does not have any client data collection and analysis modules installed')
			return(501, 'This server does not have any data collection and analysis modules installed')
