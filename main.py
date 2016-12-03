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
	def post(self):#TODO: use request.body and json
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
		self.write((yield rec.rec.gTrust(payload['sessionID'],
			payload['userID'], site, db)))

class apiRegisterUser(tornado.web.RequestHandler):
	@gen.coroutine
	def post(self):
		payload = json.loads(self.request.body.decode('utf-8'))
		db = self.settings['db']
		out = yield rec.rec.copyData(payload, db)
		self.set_status(out[0])
		self.write(out[1])

class collect(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", 'application/javascript; charset="utf-8"')
		self.render('collect.js', collectors=rec.mods.fxns,
			colList = json.dumps(rec.mods.fxnNames))

db = motor.motor_tornado.MotorClient().hijackingPrevention

def makeApp():
	return(tornado.web.Application([
		(r"/api/sub_dat", apiSubmitData),
		(r"/api/get_trust", apiGetTrust),
		(r"/api/reg_usr", apiRegisterUser),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static/'}),
		(r"/dynamic/collect.js", collect)
	], db=db, template_path='templates/'))

if __name__ == '__main__':
	app = makeApp()
	app.listen(8080)
	tornado.ioloop.IOLoop.current().start()
