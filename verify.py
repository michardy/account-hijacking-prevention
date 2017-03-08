#module that generates and emails device adding codes

import smtplib
import hashlib
import user
import os
import base64
from tornado import gen

@gen.coroutine
def makeCode(uid, sid, site, db):
	secret = base64.b32encode(os.urandom(10))
	#email code
	code = hashlib.sha512(secret + uid + sid + site)
	member = user.User(uid, site, db)
	yield memeber.read_db()
	member.code = code
	member.write_out()

@gen.coroutine
def valCode(secret, uid, sid, site, db):
	member = user.User(uid, site, db)
	yield memeber.read_db()
	return(member.code == hashlib.sha512(secret + uid + sid + site))
