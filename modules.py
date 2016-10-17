import api

def receiver():
	global rec
	rec = api.receiver()

#this file needs to be split up to avoid cyclic imports

import ip_adress_checker
