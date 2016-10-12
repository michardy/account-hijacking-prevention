import tornado.ioloop, tornado.web, motor.motor_tornado, api

rec = api.receiver() #setup mongod interface here

class api_submit_data(tornado.web.RequestHandler):
	def get(self):
		rec.add_data(self)

class api_get_trust(tornado.web.RequestHandler):
	def get(self):
		self.write(rec.run(self.get_argument('sessionID'),
			self.get_argument('userID')))

def make_app():
	return(tornado.web.Application([
		(r"/api/sub_dat", api_submit_data),
		(r"/api/get_trust", api_get_trust),

	]))

if __name__ == '__main__':
	app = make_app()
	app.listen(8080)
	tornado.ioloop.IOLoop.current().start()
