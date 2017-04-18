import pathfix
pathfix.fixpath()

import bcrypt

from tornado import gen

import modules.fingerprint as fingerprint
import modules.ip_address_checker as ip_address_checker
import modules.keystroke_dynamics as keystroke_dynamics

class Launderer():
	'''Returns data in a way that circumvents pytest's aversion to yielding'''
	def __init__(self, hasher, first, second, third, arg_number):
		self.hash = ''
		self.__hasher = hasher
		self.__first = first
		self.__second = second
		self.__third = third
		self.__arg_number = arg_number
	@gen.coroutine
	def invoke_untouchable(self):
		'''Do what Pytest will not'''
		if self.__arg_number == 3:
			self.hash = yield self.__hasher(self.__first, self.__second, self.__third)
		elif self.__arg_number == 2:
			self.hash = yield self.__hasher(self.__first, self.__second)
		else:
			self.hash = yield self.__hasher(self.__first)

def test_fingerprint_hasher():
	'''Tests fingerprint module hasher'''
	launderer = Launderer(fingerprint.hasher, 'fake_data', {}, b'$2b$12$be22kDNa1.ZduxRmhfJWoO', 3)
	launderer.invoke_untouchable()
	assert launderer.hash == b'$2b$12$be22kDNa1.ZduxRmhfJWoOmQZBb1hlO1972OO70yZhTpX2o02VN3m'

def test_fingerprint_translator():
	'''Tests fingerprint module translator'''
	launderer = Launderer(fingerprint.translator, b'fake_data', None, None, 1)
	launderer.invoke_untouchable()
	assert bcrypt.hashpw(b'fake_data', launderer.hash) == launderer.hash

def test_ip_address_checker_hasher():
	'''Tests ip_address module hasher'''
	launderer = Launderer(ip_address_checker.hasher, '', {'X-Real-IP':'fake_data'}, b'$2b$12$be22kDNa1.ZduxRmhfJWoO', 3)
	launderer.invoke_untouchable()
	assert launderer.hash == b'$2b$12$be22kDNa1.ZduxRmhfJWoOmQZBb1hlO1972OO70yZhTpX2o02VN3m'

def test_ip_address_checker_translator():
	'''Tests ip_address module translator'''
	launderer = Launderer(ip_address_checker.translator, b'fake_data', None, None, 1)
	launderer.invoke_untouchable()
	assert bcrypt.hashpw(b'fake_data', launderer.hash) == launderer.hash

def test_keystroke_dynamics_hasher():
	'''Tests keystroke_dynamics hasher'''
	data = {
		'1.2': '1.3',
		'1.4': '1.5'
	}
	launderer = Launderer(keystroke_dynamics.hasher, data, {}, b'$2b$12$be22kDNa1.ZduxRmhfJWoO', 3)
	launderer.invoke_untouchable()
	assert launderer.hash == {'1_2':'1.3','1_4':'1.5'}


def test_keystroke_dynamics_translator():
	'''Tests ip_address module translator'''
	launderer = Launderer(keystroke_dynamics.translator, {'1_2':'1.3','1_4':'1.5'}, None, None, 1)
	launderer.invoke_untouchable()
	assert {'1_2':'1.3','1_4':'1.5'} == launderer.hash


def test_keystroke_dynamics_comparer():
	'''Tests ip_address module comparer for perfect user'''
	launderer = Launderer(keystroke_dynamics.comparer, {'1_2':'13','1_4':'15'}, {'1_2':'13','1_4':'15'}, None, 2)
	launderer.invoke_untouchable()
	assert launderer.hash == 1
