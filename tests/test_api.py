#Fixes pytest path problems
#May break the Python interpreter's ability to run this program
import sys
import os
corrected_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, corrected_path + '/../')

#from unittest.mock import MagicMock, Mock

import datetime

from tornado import gen

import hijackingprevention.api as api

class FakeCollection():
	'''Fake MongoDB collection object'''
	def __init__(self, found_object):
		'''Setup function access to __init__ is blocked by use of Mock as child class'''
		self.__found = found_object
		self.finder_call = {}
		self.replacer_called = False
	@gen.coroutine
	def find_one(self, d_obj):
		'''Emulates the retrieval of a document'''
		self.finder_call = d_obj
		return(self.__found)
	@gen.coroutine
	def find_one_and_replace(self, target, d_obj, upsert):
		'''emulates find_one_and_replace and checks attributes including expiretime'''
		self.replacer_called = True

@gen.coroutine
def fake_hasher(data, key, headers, salt):
	'''Emulates a hasher function'''
	assert data == 'fake_data'
	assert salt == b'fake_salt'
	assert headers.get('Host') == headers.get('X-Real-IP')
	return(str(data)+str(salt)+str(headers.get('X-Real-IP')))

def test_api_add_data():
	headers = {'Host':'127.0.0.1', 'X-Real-IP': '127.0.0.1'}

	rec = api.Receiver()
	rec.add_hasher('fake_data', fake_hasher)
	print(rec.__dict__)

	req = {'name':'fake_data', 'ck':'fake_ck', 'sessionID':'fake_sid', 'data':'fake_data'}

	fake_site_list = FakeCollection({
		'clientKey':'fake_ck',
		'_id':'fake_id',
		'salts':{'fake_data':'fake_salt'},
		'host':'127.0.0.1',
		'serverKey':'irrelivant_server_key'
	})
	fake_site_data = FakeCollection({
		'sid':'fake_sid',
		'_id':'fake_id',
		'data':{},
		'expireTimes':{}
	})
	#fake_collection.find_one = MagicMock()
	#fake_collection.find_one_and_replace = MagicMock()
	db = {
		'siteList':fake_site_list,
		'sessionData_site-fake_id':fake_site_data
	}

	rec.add_data(req, headers, db)
	assert fake_site_list.finder_call == {'clientKey':'fake_ck'}
	assert fake_site_data.replacer_called
