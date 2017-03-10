import logging
from tornado import gen

import db_int

logger = logging.getLogger(__name__)

class Site(db_int.Interface):
	"""This class handles reading site attributes from the database."""
	def __init__(self, db):
		self.__salts = {}
		self.__id_type = '_id'
		self.__id = None
		self.__data_type = "siteList"
		self.__host = None
		self.__client_key = None
		self.__server_key = None
		self.__db = db

	@gen.coroutine
	def get_by_client_key(self, key, host):
		"""Get site based on web client API key."""
		sl = self.__db[self.__data_type]
		site = yield sl.find_one({'clientKey':key})
		if site['host'] == host:
			self.__id = site['_id']
			self.__salts = site['salts']
			self.__host = site['host']
			self.__client_key = site['clientKey']
			self.__server_key = site['serverKey']

	@gen.coroutine
	def get_by_server_key(self, key):
		"""Get site based on server API key."""
		sl = self.__db[self.__data_type]
		site = yield sl.find_one({'serverKey':key})
		self.__id = site['_id']
		self.__salts = site['salts']
		self.__host = site['host']
		self.__client_key = site['clientKey']
		self.__server_key = site['serverKey']

	def get_id(self):
		"""Get site database ID"""
		return(self.__id)

	def get_salt(self, type):
		"""Get sitewide salt for given data type"""
		return(self.__salts[type])

	def __combine(self):
		"""Return dictionary reepresentation of class"""
		return({self.__id_type:self.__id, 'salts':self.__salts,
			'host':self.__host, 'clientKey':self.__client_key,
			'serverKey':self.__server_key})
