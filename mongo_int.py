# This file handles reading and writing data to the databse
import datetime
from tornado import gen

@gen.coroutine
def getSiteByClientKey(key, ref, db):
	sl = db['siteList']
	site = yield sl.find_one({'clientKey':key})
	return(str(site['_id']))

@gen.coroutine
def getSiteByServerKey(key, ref, db):
	sl = db['siteList']
	site = yield sl.find_one({'serverKey':key})
	return(site['_id'])

def session_update(session, data, type):
	session[type]['data'] = data
	curTime = datetime.datetime.utcnow()
	tDelta = datetime.timedelta(hours=60)
	session[type]['expireTime'] = curTime + tDelta #set the data to expire in an hour
	return(session)

@gen.coroutine
def getSalt(key, ref, db, type):
	sl = db['siteList']
	site = yield sl.find_one({'clientKey':key})
	return(site['salts'][type])

@gen.coroutine
def addToSession(data, type, session, site, db):
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

def sessionToUser(SID, UID, site):
	ssd = db['sessionData_site-' + site]
	sud = db['userData_site-' + site]
	result = ssd.find_one({'sessionID':session})
	if result:
		result.pop('sessionID', None)
		result['userID'] = UID
		sud.insert(result)
