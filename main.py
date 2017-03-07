#! venv/bin/python
# This script is the main script
# It responds to HTTP requests

import tornado.ioloop
import tornado.web
import motor.motor_tornado
import json
import logging
import rec #TODO: rename to modules
import config
import client
import mongo_int
import verify
from tornado import gen

logger = logging.getLogger()

class ApiSubmitData(tornado.web.RequestHandler):
	"""Receives data submitted by collect.js and send.js"""
	@gen.coroutine
	def post(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		payload = json.loads(self.request.body.decode('utf-8'))
		db = self.settings['db']
		out = yield rec.rec.add_data(payload, self.request.headers, db)
		self.set_status(out[0])
		self.write(out[1])

class ApiGetTrust(tornado.web.RequestHandler):
	"""Handles API call to calculate user trust score."""
	@gen.coroutine
	def post(self):
		db = self.settings['db']
		payload = json.loads(self.request.body.decode('utf-8'))
		site = yield mongo_int.get_site_by_server_key(payload['ak'], db)
		if site:
			trust = (yield rec.rec.get_trust(payload['sid'],
				payload['uid'], site, db))
			self.set_status(trust[0])
			self.write(trust[1])
		else:
			self.set_status(401)
			self.write('Unauthorised')
			logger.warning('Attempted Unauthorised Access from: ' + self.request.remote_ip)

class ApiRegisterUser(tornado.web.RequestHandler):
	"""Handles API call to register or update a user"""
	@gen.coroutine
	def post(self):
		payload = json.loads(self.request.body.decode('utf-8'))
		db = self.settings['db']
		out = yield rec.rec.copy_data(payload, db)
		self.set_status(out[0])
		self.write(out[1])

class ApiValUsr(tornado.web.RequestHandler):
	"""Handles API call to send a confirmation code by email."""
	def post(self):
		db = self.settings['db']
		payload = json.loads(self.request.body.decode('utf-8'))
		site = yield mongo_int.get_site_by_server_key(payload['ak'], db)
		verify.makeCode(uid, sid, site, db)
		return('OK')

class ApiValCode(tornado.web.RequestHandler):
	"""Handels API call to validate confirmation code."""
	def post(self):
		db = self.settings['db']
		site = yield mongo_int.get_site_by_client_key(self.get_argument('ck'))
		uid = self.get_argument('uid')
		sid = self.get_argument('sid')
		#code = yield mongo_int.getUserValCode(uid, site)
		if code == self.get_argument('code'):
			pass
			#yield rec.rec.copyData({'sid':sid, 'uid':uid}, db)

class Collect(tornado.web.RequestHandler):
	"""Renders template of collect.js"""
	def get(self):
		self.set_header("Content-Type", 'application/javascript; charset="utf-8"')
		self.render('collect.js', collectors=rec.mods.fxns,
			col_list = json.dumps(rec.mods.fxnNames))

class TestPage(tornado.web.RequestHandler):
	"""Renders Welcome Page"""
	def get(self):
		self.render('index.html')

class AskUser(tornado.web.RequestHandler):
	"""Renders template of confirmation code submission page"""
	def get(self):
		self.render('verify.html', sid=self.get_argument('sid'),
			ck=self.get_argument('ck'))

db = motor.motor_tornado.MotorClient().hijackingPrevention

def makeApp():
	return(tornado.web.Application([
		(r"/api/sub_dat", ApiSubmitData),
		(r"/api/get_trust", ApiGetTrust),
		(r"/api/reg_usr", ApiRegisterUser),
		(r"/api/val_usr", ApiValUsr),
		(r"/api/val_code", ApiValCode),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static/'}),
		(r"/dynamic/collect.js", Collect),
		(r"/", TestPage),
		(r"/dynamic/ask_usr", AskUser)
	], db=db, template_path='templates/'))

if __name__ == '__main__':
	app = makeApp()
	app.listen(8080)
	tornado.ioloop.IOLoop.current().start()
