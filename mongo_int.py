# This file handles reading and writing data to the databse
import datetime
import base64
import logging
from tornado import gen

logger = logging.getLogger(__name__)

@gen.coroutine
def getSiteByClientKey(key, ref, db):
	sl = db['siteList']
	site = yield sl.find_one({'clientKey':key})
	return(str(site['_id']))

@gen.coroutine
def getSiteByServerKey(key, db):
	sl = db['siteList']
	site = yield sl.find_one({'serverKey':key})
	return(site['_id'])

def session_update(session, data, type):
	session[type]['data'] = data
	curTime = datetime.datetime.utcnow()
	tDelta = datetime.timedelta(hours=1)
	session[type]['expireTime'] = curTime + tDelta #set the data to expire in an hour
	return(session)

@gen.coroutine
def getSalt(key, ref, db, type):
	sl = db['siteList']
	site = yield sl.find_one({'clientKey':key})
	return(base64.b64decode(site['salts'][type]))

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

@gen.coroutine
def getSession(sid, site, db):
	ssd = db['sessionData_site-' + str(site)]
	rdat = (yield ssd.find_one({'sessionID':sid}))['data']
	out = {}
	for k in rdat.keys():
		if rdat[k]['expireTime'] > datetime.datetime.utcnow():
			out[k] = rdat[k]
	return(out)

@gen.coroutine
def getUserDat(uid, site, db):
	sud = db['userData_site-' + str(site)]
	return((yield sud.find_one({'uid':uid}))['data'])

@gen.coroutine
def writeUser(uid, data, site, db):
	sud = db['userData_site-' + str(site)]
	try:
		res = sud.findOne({'uid':uid})
	except TypeError:
		res = False
	if not res:
		res = {'uid':uid, 'data':{}}
	print(data)
	print(res)
	for k in data['data'].keys():
		if k in res['data'].keys():
			res['data'][k].append(data['data'][k])
		else:
			res['data'][k] = [data['data'][k]]
	sud.find_one_and_replace({'uid':uid}, res, upsert=True)
	#check if the user already exists
	#if so merge their data

@gen.coroutine
def setUserCode(code, uid, site, db):
	suc = db['userCodes_site-' + str(site)]
	suc.find_one_and_replace({'userID':uid}, {'userID':uid, 'code':code}, upsert=True)

@gen.coroutine
def getUserCode(uid, site, db):
	suc = db['userCodes_site-' + str(site)]
	user = suc.findOne({'uid':uid})
	return(user['code'])

def sessionToUser(SID, UID, site):
	ssd = db['sessionData_site-' + site]
	sud = db['userData_site-' + site]
	result = ssd.find_one({'sessionID':session})
	if result:
		result.pop('sessionID', None)
		result['userID'] = UID
		sud.insert(result)
