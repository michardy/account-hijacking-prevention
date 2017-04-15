# The primary purpose of this module is to run data hashing and comparison functions
# It is also called during the intialization of modules to register their hashing and comparison functions.

import hijackingprevention.user as user
import hijackingprevention.session as session
import hijackingprevention.api_user as api_user

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
		self.__async = {}

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
		if req['name'] in self.__hashers.keys():
			#setup to invoke hasher
			site = api_user.Site(db)
			yield site.get_by_client_key(req['ck'],
				headers.get("Host"))
			salt = site.get_salt(req['name'])
			#invoke hasher
			hash = yield self.__hashers[req['name']](req['data'],
				headers, salt)
			#store the result
			site_id = site.get_id()
			ses = session.Session(req['sessionID'], site_id, db) #setup session object
			yield ses.read_db() #read session if it exists
			ses.add_data({req['name']:hash}) #add data to session object
			yield ses.write_out() #update session object in database
			return(OK) #Nothing failed. Right? oops.
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
				temp = (yield self.__comparers[data_type](
					sdat[data_type], h))
				if temp > sub_tot: #fix security issue created by the previous ability to combine multiple low scores
					sub_tot = temp
		elif data_type not in sdat: #the user's session data may have expired or have not been collected
			sub_tot = -1*self.__maxscores[data_type] #score nonexistant data negativly
		return(sub_tot)

	@gen.coroutine
	def get_trust(self, sdat, mdat, site, db):
		"""This scores how trustworthy a user is as a number between -1 and 1.
		The score is based on how much session data matches the data stored in their user profile.
		A score of 1 means that the user is perfectly trustworthy, a score of 0 means they cannot be trusted.
		A negative score means that the users data has expired and an accurate determination cannot be made.
		"""
		total = 0 #total user score
		actmax = 0 #maximum achievable total (A user with this score is PERFECT)
		for dt in self.__comparers.keys(): #loop through all the types of data
			actmax += self.__maxscores[dt] #add data type's max score to the maximum
			total += yield self.__calculate_sub_rating(dt, sdat, mdat) #calculate sub score for given data type and add it to total
		try:
			return(200, str(total/actmax))
		except ZeroDivisionError:
			logger.critical('This server does not have any client data collection and analysis modules installed')
			return(501, 'This server does not have any data collection and analysis modules installed')
