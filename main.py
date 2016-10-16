# This script is the main script
# It responds to HTTP requests and connects to the server

import tornado.ioloop
import tornado.web
import motor.motor_tornado
import api

rec = api.receiver()

class apiSubmitData(tornado.web.RequestHandler):
	def get(self):
		rec.addData(self)

class apiGetTrust(tornado.web.RequestHandler):
	def get(self):
		db = self.settings['db']
		self.write(rec.gTrust(self.get_argument('sessionID'),
			self.get_argument('userID'), db))

db = motor.motor_tornado.MotorClient().hijackingPrevention

def makeApp():
	return(tornado.web.Application([
		(r"/api/sub_dat", apiSubmitData),
		(r"/api/get_trust", apiGetTrust),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static/'})
	], db=db))

if __name__ == '__main__':
	app = makeApp()
	app.listen(8080)
	tornado.ioloop.IOLoop.current().start()
