class Interface():
	"""Generic databse interface"""
	@gen.coroutine
	def write_out(self):
		"""Generic write function"""
		table = self.__db[self.__data_type + self.__site]
		target = {self.__id_type:self.__id}
		out = self.__combine()
		table.find_one_and_replace(target, out, upsert=True)
