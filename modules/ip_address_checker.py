import bcrypt
import rec
import hashlib
import mongo_int
from tornado import gen

import logging
logger = logging.getLogger(__name__)

@gen.coroutine
def hasher(data, key, headers, db):
	salt = yield mongo_int.get_salt(key, headers.get('Host'), db,
		'ip')
	ip = headers.get('X-Real-IP')
	return(hashlib.sha512(ip.encode('utf-8') + salt).hexdigest())

rec.rec.add_hasher('ip', hasher)

@gen.coroutine
def comparer(session, user, site, db):
	try:
		for h in user['ip']:
			if bcrypt.hashpw(session['ip']['data'].encode('utf-8'), h) == h:
				return(True)
		return(False)
	except KeyError:
		logger.error('User session data expired')
		return(0)

rec.rec.add_comparer('ip', comparer, 1)

def translator(data):
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(data['data'].encode('utf-8'), salt))

rec.rec.add_translator('ip', translator)

fxn = '''
function ip(){
	return(['ip', 'ip']);
}
'''

rec.mods.add('ip', fxn)
