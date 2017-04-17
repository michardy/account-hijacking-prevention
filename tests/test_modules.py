import pathfix
pathfix.fixpath()

from tornado import gen

import modules.fingerprint as fingerprint
import modules.ip_address_checker as ip_address_checker

class Launderer():
	'''Returns data in a way that circumvents pytest's aversion to yielding'''
	def __init__(self, hasher):
		self.hash = ''
		self.__hasher = hasher
	@gen.coroutine
	def invoke_untouchable(self):
		'''Do what Pytest will not'''
		salt = b'$2b$12$be22kDNa1.ZduxRmhfJWoO'
		data = 'fake_data'
		headers = {'X-Real-IP':'fake_data'}
		self.hash = yield self.__hasher(data, headers, salt)

def test_fingerprint_hasher():
	launderer = Launderer(fingerprint.hasher)
	launderer.invoke_untouchable()
	assert launderer.hash == b'$2b$12$be22kDNa1.ZduxRmhfJWoOmQZBb1hlO1972OO70yZhTpX2o02VN3m'

def test_ip_address_checker_hasher():
	launderer = Launderer(ip_address_checker.hasher)
	launderer.invoke_untouchable()
	assert launderer.hash == b'$2b$12$be22kDNa1.ZduxRmhfJWoOmQZBb1hlO1972OO70yZhTpX2o02VN3m'
