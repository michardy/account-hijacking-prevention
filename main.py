#! venv/bin/python
# This script is the main script
# It responds to HTTP requests and connects to the server

import tornado.ioloop
import tornado.web
import motor.motor_tornado
import json
import rec #rename modules
import config
import client
import mongo_int
from tornado import gen

class apiSubmitData(tornado.web.RequestHandler):
	@gen.coroutine
	def post(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		payload = json.loads(self.request.body.decode('utf-8'))
		db = self.settings['db']
		out = yield rec.rec.addData(payload, db)
		self.set_status(out[0])
		self.write(out[1])

class apiGetTrust(tornado.web.RequestHandler):
	@gen.coroutine
	def post(self):
		db = self.settings['db']
		payload = json.loads(self.request.body.decode('utf-8'))
		site = yield mongo_int.getSiteByServerKey(payload['ak'], db)
		self.write((yield rec.rec.gTrust(payload['sid'],
			payload['uid'], site, db)))

class apiRegisterUser(tornado.web.RequestHandler):
	@gen.coroutine
	def post(self):
		payload = json.loads(self.request.body.decode('utf-8'))
		db = self.settings['db']
		out = yield rec.rec.copyData(payload, db)
		self.set_status(out[0])
		self.write(out[1])

class apiValUsr(tornado.web.RequestHandler):
	def post(self):
		db = self.settings['db']
		payload = json.loads(self.request.body.decode('utf-8'))
		#email.confirm(payload['email'], code)
		#mongo_int.storeUserValCode(code, payload['uid'],
		#	payload['ak'], db)
		return('OK')

class apiValCode(tornado.web.RequestHandler):
	def post(self):
		db = self.settings['db']
		site = yield mongo_int.getSiteByClientKey(self.get_argument('ck'))
		uid = self.get_argument('uid')
		sid = self.get_argument('sid')
		#code = yield mongo_int.getUserValCode(uid, site)
		if code == self.get_argument('code'):
			pass
			#yield rec.rec.copyData({'sid':sid, 'uid':uid}, db)

class collect(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", 'application/javascript; charset="utf-8"')
		self.render('collect.js', collectors=rec.mods.fxns,
			colList = json.dumps(rec.mods.fxnNames))

class testpage(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

class askUser(tornado.web.RequestHandler):
	def get(self):
		self.render('verify.html', sid=self.get_argument('sid'),
			ck=self.get_argument('ck'))

db = motor.motor_tornado.MotorClient().hijackingPrevention

def makeApp():
	return(tornado.web.Application([
		(r"/api/sub_dat", apiSubmitData),
		(r"/api/get_trust", apiGetTrust),
		(r"/api/reg_usr", apiRegisterUser),
		(r"/api/val_usr", apiValUsr),
		(r"/api/val_code", apiValCode),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static/'}),
		(r"/dynamic/collect.js", collect),
		(r"/", testpage),
		(r"/dynamic/ask_usr", askUser)
	], db=db, template_path='templates/'))

if __name__ == '__main__':
	app = makeApp()
	app.listen(8080)
	tornado.ioloop.IOLoop.current().start()
