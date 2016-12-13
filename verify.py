import smtplib
import hashlib
import mongo_int
import os
import base64
from tornado import gen

@gen.coroutine
def makeCode(uid, sid, site, db):
	secret = base64.b32encode(os.urandom(10))
	#email code
	code = hashlib.sha512(secret + uid + sid + site)
	mongo_int.setUserCode(code, uid, site, db)

@gen.coroutine
def valCode(secret, uid, sid, site, db):
	hash = yield mongo_int.getUserCode(uid, site, db)
	return(hash == hashlib.sha512(secret + uid + sid + site))
