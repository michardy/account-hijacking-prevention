class Interface():
	"""Generic databse interface"""
	@gen.coroutine
	def write_out(self, site, db):
		"""Generic write function"""
		table = db[self.__data_type + str(site)]
		target = {self.__id_type:self.__id}
		out = self.__combine()
		table.find_one_and_replace(target, out, upsert=True)
