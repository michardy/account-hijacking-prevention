import bcrypt
import rec
import hashlib
import mongo_int
from tornado import gen

@gen.coroutine
def hasher(data, key, ref, db):
	salt = yield mongo_int.getSalt(key, ref, db, 'ip')
	return(hashlib.sha256(data.encode('utf-8') + salt.encode('utf-8')).hexdigest())

rec.rec.addHasher('ip', hasher)

def comparer(SID, UID, site):
	ssd = db['sessionData_site-' + site]
	sud = db['userData_site-' + site]
	session = ssd.find_one({'sessionID':SID})
	user = sud.find_one({'userID':UID})
	return(session['data'] == user['data'])

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
