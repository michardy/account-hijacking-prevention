
class Client():
	"""class that stores js functions for dynamically generated API client (collect.js)"""
	def __init__(self):
		self.fxns = []
		self.fxnNames = []
		self.async = []
	def add(self, fxn_name, script, is_async):
		"""Called to add a script to be sent with collect.js"""
		self.fxns.append(script)
		self.fxnNames.append(fxn_name)
		self.async.append(is_async)
