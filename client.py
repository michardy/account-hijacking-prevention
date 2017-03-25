
class Client():
	"""class that stores js functions for dynamically generated API client (collect.js)"""
	def __init__(self):
		self.fxns = []
		self.fxnNames = []
	def add(self, fxnName, script):
		self.fxns.append(script)
		self.fxnNames.append(fxnName)
