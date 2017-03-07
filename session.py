import datetime
import logging
from tornado import gen

import db_int

logger = logging.getLogger(__name__)


class Session(db_int.Interface):
	"""This class handles reading, writing, and manipulating session objects."""
	def __init__(self, sid, site, db):
		self.__id_type = "sid"
		self.__id = sid
		self.__data_type= 'sessionData_site-'
		self.data = {}
		self.__site = str(site)
		self.__db = db

	@gen.coroutine
	def read_db(self):
		"""Removes expired data from a session and returns the results."""
		ssd = self.__db[self.__data_type + self.__site]
		rdat = (yield ssd.find_one({'sessionID':self.__id}))['data']
		self.data = {}
		for k in rdat.keys():
			if rdat[k]['expireTime'] > datetime.datetime.utcnow():
				self.data[k] = rdat[k]

	def __update_expire_time(self, type):
		"""Updates a data field in a session to expire in an hour."""
		cur_time = datetime.datetime.utcnow()
		time_delta = datetime.timedelta(hours=1)
		self.data[type]['expireTime'] = cur_time + time_delta #set the data to expire in an hour

	def add_data(self, data):
		"""Adds data to session."""
		for k in data.keys():
			self.data[k] = data[k]
			self.__update_expire_time(type)

	def __combine(self):
		"""Returns user object as dictionary"""
		return({self.__id_type:self.__id, 'data':self.data})
