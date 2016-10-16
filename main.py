# This script is the main script
# It responds to HTTP requests and connects to the server

import tornado.ioloop, tornado.web, motor.motor_tornado, api

rec = api.receiver()

class api_submit_data(tornado.web.RequestHandler):
	def get(self):
		rec.add_data(self)

class api_get_trust(tornado.web.RequestHandler):
	def get(self):
		db = self.settings['db']
		self.write(rec.gTrust(self.get_argument('sessionID'),
			self.get_argument('userID'), db))

db = motor.motor_tornado.MotorClient().hijackingPrevention

def make_app():
	return(tornado.web.Application([
		(r"/api/sub_dat", api_submit_data),
		(r"/api/get_trust", api_get_trust),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static/'})
	], db=db))

if __name__ == '__main__':
	app = make_app()
	app.listen(8080)
	tornado.ioloop.IOLoop.current().start()
