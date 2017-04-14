import tornado.ioloop
import hijackingprevention.main as main

app = main.makeApp()
app.listen(8080)
tornado.ioloop.IOLoop.current().start()
