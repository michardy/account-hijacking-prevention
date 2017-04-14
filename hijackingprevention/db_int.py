from tornado import gen

class Interface():
	"""Generic databse interface"""
	def __init__(self, db, dt, site, idt, id, combine):
		self.__db= db
		self.__data_type = dt
		self.__site = site
		self.__id_type = idt
		self.__id = id
		self.__combine = combine

	@gen.coroutine
	def write_out(self):
		"""Generic write function"""
		table = self.__db[self.__data_type + self.__site]
		target = {self.__id_type:self.__id}
		out = self.__combine()
		table.find_one_and_replace(target, out, upsert=True)
