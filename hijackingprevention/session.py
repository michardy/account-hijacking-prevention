import datetime
import logging
from tornado import gen

import hijackingprevention.db_int as db_int

logger = logging.getLogger(__name__)


class Session(db_int.Interface):
	"""This class handles reading, writing, and manipulating session objects."""
	def __init__(self, sid, site, db):
		self.__id_type = "sid"
		self.__id = sid
		self.__data_type= 'sessionData_site-'
		self.data = {}
		self.__expire_times = {}
		self.__site = str(site)
		self.__db = db
		super(Session, self).__init__(db, self.__data_type, str(site),
			self.__id_type, sid, self.__combine)

	@gen.coroutine
	def read_db(self):
		"""Removes expired data from a session and returns the results."""
		ssd = self.__db[self.__data_type + self.__site]
		try:
			dat = (yield ssd.find_one({self.__id_type:self.__id}))
			rdat = dat['data']
			exp_dat = dat['expireTimes']
		except TypeError:
			rdat = {}
		self.data = {}
		for k in rdat.keys():
			if exp_dat[k] > datetime.datetime.utcnow():
				self.data[k] = rdat[k]
				self.__expire_times[k] = exp_dat[k]

	def __update_expire_time(self, d_type):
		"""Updates a data field in a session to expire in an hour."""
		cur_time = datetime.datetime.utcnow()
		time_delta = datetime.timedelta(hours=1)
		self.__expire_times[d_type] = cur_time + time_delta #set the data to expire in an hour

	def add_data(self, data):
		"""Adds data to session."""
		for k in data.keys():
			self.data[k] = data[k]
			self.__update_expire_time(k)

	def __combine(self):
		"""Returns user object as dictionary"""
		return({self.__id_type:self.__id, 'data':self.data,
			'expireTimes':self.__expire_times})
