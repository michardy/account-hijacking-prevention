import pathfix
pathfix.fixpath()

from tornado import gen

import modules.fingerprint as fingerprint
import modules.ip_address_checker as ip_address_checker
import modules.keystroke_dynamics as keystroke_dynamics

class Launderer():
	'''Returns data in a way that circumvents pytest's aversion to yielding'''
	def __init__(self, hasher, data):
		self.hash = ''
		self.__hasher = hasher
		self.data = data
	@gen.coroutine
	def invoke_untouchable(self):
		'''Do what Pytest will not'''
		salt = b'$2b$12$be22kDNa1.ZduxRmhfJWoO'
		headers = {'X-Real-IP':'fake_data'}
		self.hash = yield self.__hasher(self.data, headers, salt)

def test_fingerprint_hasher():
	launderer = Launderer(fingerprint.hasher, 'fake_data')
	launderer.invoke_untouchable()
	assert launderer.hash == b'$2b$12$be22kDNa1.ZduxRmhfJWoOmQZBb1hlO1972OO70yZhTpX2o02VN3m'

def test_ip_address_checker_hasher():
	launderer = Launderer(ip_address_checker.hasher, '')
	launderer.invoke_untouchable()
	assert launderer.hash == b'$2b$12$be22kDNa1.ZduxRmhfJWoOmQZBb1hlO1972OO70yZhTpX2o02VN3m'

def test_keystroke_dynamics_hasher():
	data = {
		'1.2': '1.3',
		'1.4': '1.5'
	}
	launderer = Launderer(keystroke_dynamics.hasher, data)
	launderer.invoke_untouchable()
	assert launderer.hash == {'1_2':'1.3','1_4':'1.5'}
