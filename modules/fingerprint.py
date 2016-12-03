import bcrypt
import rec
import hashlib
import mongo_int
from tornado import gen

@gen.coroutine
def hasher(data, key, ref, db):
	salt = yield mongo_int.getSalt(key, ref, db, 'fingerprint')
	return(hashlib.sha256(data.encode('utf-8') + salt.encode('utf-8')).hexdigest())

rec.rec.addHasher('fingerprint', hasher)

@gen.coroutine
def comparer(sid, uid, site, db):
	session = yield mongo_int.getSession(sid, site, db)
	user = yield mongo_int.getUserDat(uid, site, db)	
	return(bcrypt.hashpw(session['fingerprint']['data'].encode('utf-8'), user['fingerprint'][0]) == user['ip'][0])

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
