import pathfix
pathfix.fixpath()

import hijackingprevention.client as client

def test_add():
	'''Tests client.py Client.add()'''
	cli = client.Client()
	cli.add('fake_fxn_name', 'fake_js_fxn', False)
	assert cli.fxn_names == ['fake_fxn_name']
	assert cli.fxns == ['fake_js_fxn']
	assert cli.callbacks == [False]
