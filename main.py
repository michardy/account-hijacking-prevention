# This script is the main script
# It responds to HTTP requests and connects to the server

import tornado.ioloop
import tornado.web
import motor.motor_tornado
import json
import rec
import modules
import client

class apiSubmitData(tornado.web.RequestHandler):
	def post(self):#TODO: use request.body and json
		payload = json.loads(self.request.body.decode('utf-8'))
		db = self.settings['db']
		out = rec.rec.addData(payload, db)
		self.set_status(out[0])
		self.write(out[1])

class apiGetTrust(tornado.web.RequestHandler):
	def get(self):
		db = self.settings['db']
		self.write(rec.rec.gTrust(self.get_argument('sessionID'),
			self.get_argument('userID'), db))

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
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static/'}),
		(r"/dynamic/collect.js", collect)
	], db=db, template_path='templates/'))

if __name__ == '__main__':
	app = makeApp()
	app.listen(8080)
	tornado.ioloop.IOLoop.current().start()
