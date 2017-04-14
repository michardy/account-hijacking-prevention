import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from tornado import gen

import hijackingprevention.api as api

class FakeHeaders():
	def __init__(self, headers={'Host':'127.0.0.1', 'X-Real-IP': '127.0.0.1'}):
		self.headers = headers
	def get(key):
		return(self.headers[key])

class FakeCollection():
	def __init__(self):
		pass
	def fine_one(d_obj):
		assert d_obj['clientKey'] == 'fake_ck'
		return({'clientKey':'fake_ck', '_id':'irrelivant_id', 'salts':{'fake_data':'fake_salt'}, 'host':'127.0.0.1', 'serverKey':'irrelivant_server_key'})
		
@gen.coroutine
def fake_hasher(data, key, headers, salt):
	assert data == 'fake_data'
	assert salt == 'fake_salt'
	assert headers.get('Host') == headers.get('X-Real-IP')
	return(data+salt+headers.get('X-Real-IP'))

def test_api_add_data():
	headers = FakeHeaders()

	rec = api.Receiver()
	rec.add_hasher('fake_data', fake_hasher)

	req = {'name':'fake_data', 'ck':'fake_ck', 'SessionID':'fake_sid', 'data':'fake_data'}

	fake_site_list = FakeCollection()
	db = {'siteList':fake_site_list}

	rec.add_data(req, headers, db)
	

