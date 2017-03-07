# This file handles reading and writing data to the databse
import datetime
import base64
import logging
from tornado import gen

logger = logging.getLogger(__name__)

@gen.coroutine
def get_site_by_client_key(key, ref, db):
	sl = db['siteList']
	site = yield sl.find_one({'clientKey':key})
	return(str(site['_id']))

@gen.coroutine
def get_site_by_server_key(key, db):
	sl = db['siteList']
	site = yield sl.find_one({'serverKey':key})
	return(site['_id'])

def session_update(session, data, type):
	session[type]['data'] = data
	cur_time = datetime.datetime.utcnow()
	time_delta = datetime.timedelta(hours=1)
	session[type]['expireTime'] = cur_time + time_delta #set the data to expire in an hour
	return(session)

@gen.coroutine
def get_salt(key, ref, db, type):
	sl = db['siteList']
	site = yield sl.find_one({'clientKey':key})
	return(base64.b64decode(site['salts'][type]))

@gen.coroutine
def add_to_session(data, type, session, site, db):
	ssd = db['sessionData_site-' + site]
	result = yield ssd.find_one({'sessionID':session})
	if result:
		dataObj = result['data']
	else:
		dataObj = {}
	dataObj[type] = {}
	dataObj[type]['data'] = data
	dataObj = session_update(dataObj, data, type)
	ssd.find_one_and_replace({'sessionID':session}, {'sessionID':session, 'data':dataObj}, upsert=True)

@gen.coroutine
def get_session(sid, site, db):
	ssd = db['sessionData_site-' + str(site)]
	rdat = (yield ssd.find_one({'sessionID':sid}))['data']
	out = {}
	for k in rdat.keys():
		if rdat[k]['expireTime'] > datetime.datetime.utcnow():
			out[k] = rdat[k]
	return(out)

@gen.coroutine
def get_user_dat(uid, site, db):
	sud = db['userData_site-' + str(site)]
	return((yield sud.find_one({'uid':uid}))['data'])

@gen.coroutine
def write_user(uid, data, site, db):
	sud = db['userData_site-' + str(site)]
	try:
		res = sud.findOne({'uid':uid})
	except TypeError:
		res = {'uid':uid, 'data':{}}
	for k in data.keys():
		if k in res['data'].keys() and data[k] not in res['data'][k]:
			print(res['data'][k])
			print(data[k])
			res['data'][k].append(data[k])
			print(res['data'][k])
		else:
			print(k in res['data'].keys())
			print(k)
			print(res['data'].keys())
			res['data'][k] = [data[k]]
	sud.find_one_and_replace({'uid':uid}, res, upsert=True)
	#check if the user already exists
	#if so merge their data

@gen.coroutine
def set_user_code(code, uid, site, db):
	suc = db['userCodes_site-' + str(site)]
	suc.find_one_and_replace({'userID':uid}, {'userID':uid, 'code':code}, upsert=True)

@gen.coroutine
def get_user_code(uid, site, db):
	suc = db['userCodes_site-' + str(site)]
	user = suc.findOne({'uid':uid})
	return(user['code'])

def session_to_user(SID, UID, site):
	ssd = db['sessionData_site-' + site]
	sud = db['userData_site-' + site]
	result = ssd.find_one({'sessionID':session})
	if result:
		result.pop('sessionID', None)
		result['userID'] = UID
		sud.insert(result)
