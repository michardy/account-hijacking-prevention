import logging
from tornado import gen

import db_int

logger = logging.getLogger(__name__)


class User(db_int.Interface):
	"""This class handles reading, writing, and manipulating user objects."""
	def __init__(self, uid, site, db):
		self.__id_type = "uid"
		self.__id = uid
		self.__data_type= 'userData_site-'
		self.data = {}
		self.code = None #verification token
		self.__site = str(site)
		self.__db = db

	@gen.coroutine
	def read_db(self, site):
		"""Reads user object from DB."""
		sud = self.__db[self.__id_type + self.__site]
		user = yield sud.find_one({'uid':self.__id}) #Try to find user
		if user is not None:
			self.data = user['data']
			self.code = user['code']

	def add_data(self, data):
		"""Adds data to user."""
		for k in data.keys():
			if k in self.data.keys():
				self.data[k].append(data[k])
			else:
				self.data[k] = [data[k]]

	def __combine(self):
		"""Returns user object as dictionary"""
		return({self.__id_type:self.__id, 'data':self.data,
			'code':self.code})
