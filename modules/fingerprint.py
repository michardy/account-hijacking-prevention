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
		'fingerprint')
	return(hashlib.sha512(data.encode('utf-8') + salt).hexdigest())

rec.rec.add_hasher('fingerprint', hasher)

@gen.coroutine
def comparer(session, user, site, db):
	try:
		for h in user['fingerprint']:
			if bcrypt.hashpw(session['fingerprint']['data'].encode('utf-8'), h) == h:
				return(True)
		return(False)
	except KeyError:
		logger.error('User session data expired')
		return(0)

rec.rec.add_comparer('fingerprint', comparer, 1)

def translator(data):
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(data['data'].encode('utf-8'), salt))

rec.rec.add_translator('fingerprint', translator)

fxn = '''
function fingerprint(){
	var sr = window.screen.height.toString() + window.screen.width.toString() + window.screen.availHeight.toString() + window.screen.availWidth.toString();
	return(['fingerprint', sr]);
}
'''

rec.mods.add('fingerprint', fxn)
