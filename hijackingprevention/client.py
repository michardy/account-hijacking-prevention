
class Client():
	"""class that stores js functions for dynamically generated API client (collect.js)"""
	def __init__(self):
		self.fxns = []
		self.fxn_names = []
		self.callbacks = []
	def add(self, fxn_name, script, is_callback):
		"""Called to add a script to be sent with collect.js"""
		self.fxns.append(script)
		self.fxn_names.append(fxn_name)
		self.callbacks.append(is_callback)
