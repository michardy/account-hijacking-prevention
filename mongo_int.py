# This file handles reading and writing data to the databse
import datetime
import base64
import logging
from tornado import gen

logger = logging.getLogger(__name__)

@gen.coroutine
def get_site_by_client_key(key, ref, db):
	"""Get site database ID based on web client API key."""
	sl = db['siteList']
	site = yield sl.find_one({'clientKey':key})
	return(str(site['_id']))

@gen.coroutine
def get_site_by_server_key(key, db):
	"""Get site database ID based on server API key."""
	sl = db['siteList']
	site = yield sl.find_one({'serverKey':key})
	return(site['_id'])

def session_update(session, data, type):
	"""Updates a data field in a session to expire in an hour."""
	session[type]['data'] = data
	cur_time = datetime.datetime.utcnow()
	time_delta = datetime.timedelta(hours=1)
	session[type]['expireTime'] = cur_time + time_delta #set the data to expire in an hour
	return(session)

@gen.coroutine
def get_salt(key, ref, db, type):
	"""Gets sitewide salt for specific data type."""
	sl = db['siteList']
	site = yield sl.find_one({'clientKey':key})
	return(base64.b64decode(site['salts'][type]))

@gen.coroutine
def add_to_session(data, type, session, site, db):
	"""Adds data to session."""
	ssd = db['sessionData_site-' + site]
	result = yield ssd.find_one({'sessionID':session})
	if result:
		data_obj = result['data']
	else:
		data_obj = {}
	data_obj[type] = {}
	data_obj[type]['data'] = data
	data_obj = session_update(data_obj, data, type)
	ssd.find_one_and_replace({'sessionID':session}, {'sessionID':session, 'data':data_obj}, upsert=True)

@gen.coroutine
def get_session(sid, site, db):
	"""Removes expired data from a session based and returns the results."""
	ssd = db['sessionData_site-' + str(site)]
	rdat = (yield ssd.find_one({'sessionID':sid}))['data']
	out = {}
	for k in rdat.keys():
		if rdat[k]['expireTime'] > datetime.datetime.utcnow():
			out[k] = rdat[k]
	return(out)

@gen.coroutine
def get_user_dat(uid, site, db):
	"""Returns data associated with given user ID."""
	sud = db['userData_site-' + str(site)]
	return((yield sud.find_one({'uid':uid}))['data'])

@gen.coroutine
def write_user(uid, data, site, db):
	"""This creates new users and merges new data into ones that already exist."""
	sud = db['userData_site-' + str(site)]
	try:
		res = yield sud.find_one({'uid':uid}) #Try to find user
	except TypeError:
		res = {'uid':uid, 'data':{}} #Create a user object if they dont exist
	for k in data.keys():
		if k in res['data'].keys():
			res['data'][k].append(data[k])
		else:
			res['data'][k] = [data[k]]
	sud.find_one_and_replace({'uid':uid}, res, upsert=True) #replace/create user

@gen.coroutine
def set_user_code(code, uid, site, db):
	"""Stores a user's temporary authentication code."""
	suc = db['userCodes_site-' + str(site)]
	suc.find_one_and_replace({'userID':uid}, {'userID':uid, 'code':code}, upsert=True)

@gen.coroutine
def get_user_code(uid, site, db):
	"""Retreives a user's temporary authentication code"""
	suc = db['userCodes_site-' + str(site)]
	user = suc.findOne({'uid':uid})
	return(user['code'])
