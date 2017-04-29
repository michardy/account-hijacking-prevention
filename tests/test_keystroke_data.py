import pathfix
pathfix.fixpath()

#needed by pytest
import os.path
import pytest

#needed for tests
import uuid
import json

import datetime
import tornado.ioloop
import hijackingprevention.main as main

import urllib.request as req

def sub_dat(dat, d_type, header, sid):
	'''Submits session data to API server'''
	data = {
		'ck':'testClientKey',
		'sid':sid,
		'name':d_type,
		'data':dat
	}
	request = req.Request(url='http://localhost:8080/api/sub_dat', data=json.dumps(data).encode('utf-8'))
	if header is not None:		
		request.add_header(header['key'], header['value'])
	with req.urlopen(request) as r:
		r.read()
	return(sid)

def reg_usr(sid):
	'''Registers user with random UUID using API'''
	uid = str(uuid.uuid1())
	data = {
		'sid':sid,
		'uid':uid,
		'ak':'testServerKey'
	}
	request = req.Request(url='http://localhost:8080/api/reg_usr', data=json.dumps(data).encode('utf-8'))
	with req.urlopen(request) as r:
		r.read()
	return(uid)

def get_trust(sid, uid):
	'''Gets trust that a given session matches a given user using API'''
	data = {
		'sid':sid,
		'uid':uid,
		'ak':'testServerKey'
	}
	request = req.Request(url='http://localhost:8080/api/get_trust', data=json.dumps(data).encode('utf-8'))
	with req.urlopen(request) as r:
		out = r.read()
	return(float(out))

def average(lis):
	'''Applies low pass filter to an array and averages it'''
	tot = 0
	entries = 0
	for i in lis:
		if abs(i) < 100:
			tot += i
			entries += 1
	try:
		return(tot/entries)
	except ZeroDivisionError:
		return(0)

def preprocess(data):
	'''Pre-processes imported JSON data to eliminate IPhones and sort by submitter'''
	submitters = {}
	for d in data:
		if 'iPhone' not in d['UA']:
			temp = {}
			for k in d['data'].keys():
				temp[k] = average(d['data'][k])
			if d['email'] in submitters:
				submitters[d['email']].append(temp)
			else:
				submitters[d['email']] = [temp]
	return(submitters)

def run_user_tests(submitter):
	'''Goes through the list of submitted for a given tester and scores the trustworthiness of each session based on another one.  '''
	subpass = 0
	subtotp = 0
	for ds in range(1, len(submitter)):
		sid = str(uuid.uuid1())
		sub_dat(submitter[ds], 'keystroke_dynamics', None, sid)
		uid = reg_usr(sid)
		sid = str(uuid.uuid1())
		sub_dat(submitter[ds-1], 'keystroke_dynamics', None, sid)
		res = get_trust(sid, uid)
		print(f'Pass: {res}')
		if res > 0.5:
			subpass += 1
		subtotp += 1
	return(subpass/subtotp)

class MultiUserTests():
	'''Responsible for storing and scoring pairs of different submitters'''
	def __init__(self):
		self.__last = None
	def run(self, submitter):
		''''''
		if self.__last is None:
			self.__last = submitter
			return('irrelevant')
		else:
			sid = str(uuid.uuid1())
			sub_dat(submitter[0], 'keystroke_dynamics', None, sid)
			uid = reg_usr(sid)
			sid = str(uuid.uuid1())
			sub_dat(self.__last[0], 'keystroke_dynamics', None, sid)
			res = get_trust(sid, uid)
			self.__last = None
			print(f'fail: {res}')
			return(int(res <= 0.5))

@pytest.mark.skipif(not os.path.isfile('tests/res.json'),
                    reason="requires test data")
def test_user_data():
	'''Tests the accuracy of the keystroke dynamics system with colected data.  

	Running this test REQUIRES the server to be running.  
	This testa assumes that the keystroke_dynamics module is the only module installed.  
	Uninstall all other modules before running.  

	Warning: This also creates a lot of user objects in the DB.  
	'''
	passing = 0
	totpass = 0
	failing = 0
	totfail = 0
	last = None
	laste = None
	mult_usr_test = MultiUserTests()
	with open('tests/res.json', 'r') as f:
		data = json.loads(f.read())
	submitters = preprocess(data)
	for s in submitters.keys():
		if len(submitters[s]) > 1:
			passing += run_user_tests(submitters[s])
			totpass += 1
		else:
			out = mult_usr_test.run(submitters[s])
			if type(out) == float or type(out) == int:
				failing += out
				totfail += 1
	passr = passing/totpass
	failr = failing/totfail
	print(f'Passing Rate: {passr}')
	print(f'Failing Rate: {failr}')
	assert passr > 0.8
	assert failr > 0.8
