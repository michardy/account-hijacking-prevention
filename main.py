#! venv/bin/python
# This script is the main script
# It responds to HTTP requests

import tornado.ioloop
import hijackingprevention.main as main
import hijackingprevention.prune as prune

app = main.makeApp()
app.listen(8080)
pruner = tornado.ioloop.PeriodicCallback(prune.prune_all, 86400000)
pruner.start()
tornado.ioloop.IOLoop.current().start()
