class client():
	def __init__(self):
		self.fxns = []
		self.fxnNames = []
	def add(self, fxnName, script):
		self.fxns.append(script)
		self.fxnNames.append(fxnName)
