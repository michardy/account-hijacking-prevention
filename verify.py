import smtp
import hashlib
import mongo_int
import os
import base64

def makeCode(uid, sid, site, db)
	secret = base64.b32encode(os.urandom(10))
	#email code
	code = hashlib.sha512(secret + uid + sid, site)
	#mongo_int.setUserCode(code, uid, site, db)
