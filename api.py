# The primary purpose of this module is to run data hashing and comparison functions
# It is also called during the intialization of modules to register their hashing and comparison functions.

import user
import session
import api_user

from tornado import gen

import logging
logger = logging.getLogger(__name__)

OK = (200, 'OK')

class Receiver():
	"""This class handles all requests to hash and interpret data.
	Most of the shared functionalty that underpins the API is defined here.
	Functions in here fall into two catagories:
		Functions that allow modules to register hashers or comparers.
		Functions that run the registered hashers or comparers.
	Please note:
		If a function you are considering including in this file does not invoke a hasher, translator, or comparer it may not belong in this file.
	"""
	def __init__(self):
		self.__hashers = {}
		self.__translators = {}
		self.__comparers = {}
		self.__maxscores = {}

	# Module registration functions

	def add_hasher(self, name, fxn):
		"""This is called by each module on startup to register its sitewide hasher."""
		self.__hashers[name] = fxn

	def add_translator(self, name, fxn):
		"""This is called by each module on startup to register its data translator.
		Translators hash data, which has already been hashed by a (sitewide) hasher, with a per user salt.
		"""
		self.__translators[name] = fxn

	def add_comparer(self, name, fxn, score):
		"""This is called by each module on startup to register its hash comparer."""
		self.__comparers[name] = fxn
		self.__maxscores[name] = score

	# Module users and API interface

	@gen.coroutine
	def add_data(self, req, headers, db):
		"""This function is called when data is received from a browser to hash and store the data"""
		if req['name'] in self.__comparers.keys():
			hash = yield self.__hashers[req['name']](req['data'],
				req['ck'], headers, db)
			site = api_user.Site(db)
			yield site.get_by_client_key(req['ck'],
				headers.get("Host"))
			site_id = site.get_id()
			ses = session.Session(req['sessionID'], site_id, db)
			yield ses.read_db()
			ses.add_data({req['name']:hash})
			yield ses.write_out()
			return(OK)
		else:
			logger.warning('Could not find a handler for "' + req['name'] + '"')
			return(400, 'Err: Could not find a handler for "' + req['name'] + '"')

	@gen.coroutine
	def copy_data(self, ses, uid, site_id, db):
		"""This function is called to store session data permenantly to the user profile"""
		data = {}
		for dt in ses.keys():
			data[dt] = self.__translators[dt](ses[dt])
		member = user.User(uid, site_id, db)
		yield member.read_db()
		member.add_data(data)
		yield member.write_out()
		return(OK)

	@gen.coroutine
	def __calculate_sub_rating(self, data_type, sdat, mdat):
		"""Calculate trust score for specific subtype of user data"""
		sub_tot = 0
		if data_type in mdat and data_type in sdat:
			for h in mdat[data_type]: #loop through all the user's hashed data of this type and compare it to the session
				sub_tot += (yield self.__comparers[data_type](
					sdat[data_type], h))
		elif data_type not in sdat:
			sub_tot = -1*self.__maxscores[data_type]
		return(sub_tot)

	@gen.coroutine
	def get_trust(self, sdat, mdat, site, db):
		"""This scores how trustworthy a user is as a number between -1 and 1.
		The score is based on how much session data matches the data stored in their user profile.
		A score of 1 means that the user is perfectly trustworthy, a score of 0 means they cannot be trusted.
		A negative score means that the users data has expired and an accurate determination cannot be made.
		"""
		total = 0
		actmax = 0
		for dt in self.__comparers.keys():
			actmax += self.__maxscores[dt]
			total += yield self.__calculate_sub_rating(dt, sdat, mdat)
		try:
			return(200, str(total/actmax))
		except ZeroDivisionError:
			logger.critical('This server does not have any client data collection and analysis modules installed')
			return(501, 'This server does not have any data collection and analysis modules installed')
