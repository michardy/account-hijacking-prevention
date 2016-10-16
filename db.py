# This file handles reading and writing data to the databse
import datetime

def session_update(session, data, type):
	session[type]['data'] = data
	curTime = datetime.datetime.utcnow()
	tDelta = datetime.timedelta(hours=60)
	session[type]['expireTime'] = curTime + tDelta #set the data to expire in an hour

add_to_session(data, type, session, site, db):
	ssd = db['sessionData_site-' + site.id]
	result = ssd.find_one('sessionId':session)
	if result:
		dataObj = result['data']
	else:
		dataObj = sessionData()
	dataObj = session_update(dataObj, data)
	if result:
		ssd.update({'sessionID':session}, {'data':dataObj})
	else:
		ssd.insert({'sessionID':session, 'data':dataObj})
