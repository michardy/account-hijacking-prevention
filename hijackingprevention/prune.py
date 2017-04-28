import motor.motor_tornado

import datetime

from tornado import gen


@gen.coroutine
def strip_session(ses):
	'''Clean expired data from session object'''
	for k in list(ses['expireTimes']):
		if ses['expireTimes'][k] <= datetime.datetime.utcnow():
			ses['data'].pop(k, None)
			ses['expireTimes'].pop(k, None)
	return(ses)

@gen.coroutine
def prune_site(site, db):
	'''Prune expired data from site collection'''
	ses_data_col = db['sessionData_site-'+str(site)]
	ses_data = ses_data_col.find()
	while (yield ses_data.fetch_next):
		doc = ses_data.next_object()
		doc = yield strip_session(doc)
		if doc['data']:
			ses_data_col.find_one_and_replace({'_id':doc['_id']}, doc)
		else:
			ses_data_col.delete_one({'_id':doc['_id']})
	

@gen.coroutine
def prune_all():
	'''Prune expired data from all site collections'''
	db = motor.motor_tornado.MotorClient().hijackingPrevention
	site_list = db['siteList']
	sites = site_list.find()
	while (yield sites.fetch_next):
		doc = sites.next_object()
		yield prune_site(doc['_id'], db)
