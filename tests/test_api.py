import pathfix
pathfix.fixpath()

import datetime

from tornado import gen

import hijackingprevention.api as api

class FakeCollection():
	'''Fake MongoDB collection object'''
	def __init__(self, found_object):
		'''Setup function access to __init__ is blocked by use of Mock as child class'''
		self.__found = found_object
		self.finder_call = {}
		self.replacer_call = {}
	@gen.coroutine
	def find_one(self, d_obj):
		'''Emulates the retrieval of a document'''
		self.finder_call = d_obj
		return(self.__found)
	@gen.coroutine
	def find_one_and_replace(self, target, d_obj, upsert):
		'''emulates find_one_and_replace and checks attributes including expiretime'''
		print(d_obj)
		self.replacer_call = d_obj

class FakeDBObject():
	'''Misc databse classes like User and Session'''
	def __init__(self):
		self.added_data = {}
	@gen.coroutine
	def add_data(self, data):
		'''Emulates add_data'''
		self.added_data = data

@gen.coroutine
def fake_hasher(data, headers, salt):
	'''Emulates a hasher function'''
	assert data == 'fake_data'
	assert salt == b'fake_salt'
	assert headers.get('Host') == headers.get('X-Real-IP')
	return('hashed_fake_data')

@gen.coroutine
def fake_translator(data):
	assert data == 'fake_data'
	return('translated_fake_data')

@gen.coroutine
def fake_comparer(ses_hash, usr_hash):
	return(ses_hash == usr_hash)#in reality we would rehash the session data

def test_api_add_data():
	'''Tests the add_data method of the api class'''
	headers = {'Host':'127.0.0.1', 'X-Real-IP': '127.0.0.1'}

	rec = api.Receiver()
	rec.add_hasher('fake_data', fake_hasher)

	req = {'name':'fake_data', 'ck':'fake_ck', 'sid':'fake_sid', 'data':'fake_data'}

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
	db = {
		'siteList':fake_site_list,
		'sessionData_site-fake_id':fake_site_data
	}

	rec.add_data(req, headers, db)
	assert fake_site_list.finder_call == {'clientKey':'fake_ck'}
	assert fake_site_data.finder_call == {'sid':'fake_sid'}
	assert fake_site_data.replacer_call['sid'] == 'fake_sid'
	assert fake_site_data.replacer_call['data'] == {'fake_data':'hashed_fake_data'}
	curtime = datetime.datetime.utcnow()
	hour = datetime.timedelta(hours=1)
	newtime = hour + curtime
	assert fake_site_data.replacer_call['expireTimes']['fake_data'] < newtime
	assert fake_site_data.replacer_call['expireTimes']['fake_data'] > curtime

def test_api_copy_data():
	'''Tests the copy_data method of the api class'''
	rec = api.Receiver()
	rec.add_translator('fake_data_type', fake_translator)
	ses = {'fake_data_type':'fake_data'}
	fake_user_data = FakeDBObject()
	'''{
		'uid':'fake_uid',
		'_id':'fake_id',
		'data':{}
	})'''
	rec.copy_data(ses, fake_user_data)
	assert fake_user_data.added_data == {'fake_data_type':'translated_fake_data'}


class Launderer(): #PyTest will not let test functions touch a yield statment so it must be done indirectly
	'''Attempts to deal with the fact that pytest cannot interface with tornado.gen coroutines
	Q: Does it really need to be a class?
	A: I tried a function and it still did not work.  
	Q: would you like to apologize.
	A: I applagize.   
	'''
	def __init__(self, rec):
		self.__rec = rec
		self.score = ''
		self.status = 0
	@gen.coroutine
	def invoke_untouchable(self):
		'''Call the function that needs a yield'''
		session_data = {
			'fake_data_type_passing_1':'fake_data1',
			'fake_data_type_passing_2':'fake_data2'
		}
		user_data = {
			'fake_data_type_expired':['fake_data'],
			'fake_data_type_passing_1':['fake_data1', 'fake_data', 'fake_fake_data'],
			'fake_data_type_passing_2':['fake_data2', 'fake_data']
		}
		out = yield self.__rec.get_trust(session_data, user_data)
		self.score = out[1]
		self.status = out[0]
	
def test_api_get_trust():
	'''Tests api.py get_trust'''
	rec = api.Receiver()
	rec.add_comparer('fake_data_type_expired', fake_comparer, 1)
	rec.add_comparer('fake_data_type_passing_1', fake_comparer, 1)
	rec.add_comparer('fake_data_type_passing_2', fake_comparer, 1)
	rec.add_comparer('fake_data_type_missing', fake_comparer, 1)
	launderer = Launderer(rec)
	launderer.invoke_untouchable()
	assert launderer.status == 200
	assert launderer.score == '0.25'

def test_api_get_trust_no_modules():
	'''Tests that api.py get_trust fails when not supplied modules'''
	rec = api.Receiver()
	launderer = Launderer(rec)
	launderer.invoke_untouchable()
	assert launderer.status == 501
	assert launderer.score == 'This server does not have any data collection and analysis modules installed'
