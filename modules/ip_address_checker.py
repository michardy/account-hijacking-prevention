import bcrypt
import rec
import hashlib
import mongo_int
from tornado import gen

import logging
logger = logging.getLogger(__name__)

@gen.coroutine
def hasher(data, key, ref, db):
	salt = yield mongo_int.getSalt(key, ref, db, 'ip')
	return(hashlib.sha512(data.encode('utf-8') + salt).hexdigest())

rec.rec.addHasher('ip', hasher)

@gen.coroutine
def comparer(sid, uid, site, db):
	session = yield mongo_int.getSession(sid, site, db)
	user = yield mongo_int.getUserDat(uid, site, db)
	try:
		return(bcrypt.hashpw(session['ip']['data'].encode('utf-8'), user['ip'][0]) == user['ip'][0])
	except IndexError:
		logger.error('User session data expired')
		return(0)

rec.rec.addComparer('ip', comparer, 1)

def translator(data):
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(data['data'].encode('utf-8'), salt))

rec.rec.addTranslator('ip', translator)

fxn = '''
function ip(){
	return(['ip', 'ip']);
}
'''

rec.mods.add('ip', fxn)
