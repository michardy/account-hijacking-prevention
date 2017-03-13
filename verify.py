#module that generates and emails device adding codes

import smtplib
import hashlib
import user
import os
import base64
from tornado import gen
from cryptography.fernet import Fernet


@gen.coroutine
def makeCode(uid, sid, site, key, db):
	"""Make verification code and email to user."""
	secret = base64.b32encode(os.urandom(10))
	f = Fernet(key)
	#email code
	code = f.encrypt(secret + uid + sid + site)
	member = user.User(uid, site, db)
	yield memeber.read_db()
	member.code = secret
	member.write_out()

@gen.coroutine
def valCode(code, uid, sid, site, key, db):
	"""Check the varification code."""
	member = user.User(uid, site, db)
	yield memeber.read_db()
	f = Fernet(key)
	return(f.decrypt(code, 3600) == member.code + uid + sid + site)
