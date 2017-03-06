import bcrypt
import rec
import hashlib
import mongo_int
from tornado import gen

import logging
logger = logging.getLogger(__name__)

@gen.coroutine
def hasher(data, key, headers, db):
	salt = yield mongo_int.getSalt(key, headers.get('Host'), db,
		'fingerprint')
	return(hashlib.sha512(data.encode('utf-8') + salt).hexdigest())

rec.rec.addHasher('fingerprint', hasher)

@gen.coroutine
def comparer(sid, uid, site, db):
	session = yield mongo_int.getSession(sid, site, db)
	user = yield mongo_int.getUserDat(uid, site, db)
	try:
		return(bcrypt.hashpw(session['fingerprint']['data'].encode('utf-8'), user['fingerprint'][0]) == user['fingerprint'][0])
	except IndexError:
		logger.error('User session data expired')
		return(0)

rec.rec.addComparer('fingerprint', comparer, 1)

def translator(data):
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(data['data'].encode('utf-8'), salt))

rec.rec.addTranslator('fingerprint', translator)

fxn = '''
function fingerprint(){
	var sr = window.screen.height.toString() + window.screen.width.toString() + window.screen.availHeight.toString() + window.screen.availWidth.toString();
	return(['fingerprint', sr]);
}
'''

rec.mods.add('fingerprint', fxn)
