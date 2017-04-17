import pathfix
pathfix.fixpath()

from tornado import gen

import modules.fingerprint as fingerprint

class Launderer():
	'''Returns data in a way that circumvents pytest's aversion to yielding'''
	def __init__self(self):
		self.hash = ''
	@gen.coroutine
	def invoke_untouchable(self):
		'''Do what Pytest will not'''
		salt = b'$2b$12$be22kDNa1.ZduxRmhfJWoO'
		data = 'fake_data'
		headers = {}
		self.hash = yield fingerprint.hasher(data, headers, salt)

def test_hasher():
	launderer = Launderer()
	launderer.invoke_untouchable()
	assert launderer.hash == b'$2b$12$be22kDNa1.ZduxRmhfJWoOmQZBb1hlO1972OO70yZhTpX2o02VN3m'

