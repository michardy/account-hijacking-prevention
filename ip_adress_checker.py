import bcrypt
import rec
import hashlib
import mongo_int

def hasher(data, key, ref, db):
	salt = mongo_int.getSalt(key, ref, db, 'ip')
	print(key)
	return(hashlib.sha256(data.encode('utf-8') + salt).hexdigest())

rec.rec.addHasher('ip', hasher)

def comparer(SID, UID, site):
	ssd = db['sessionData_site-' + site]
	sud = db['userData_site-' + site]
	session = ssd.find_one({'sessionID':SID})
	user = sud.find_one({'userID':UID})
	return(session['data'] == user['data'])

rec.rec.addComparer('ip', comparer, 1)

fxn = '''
function ip(){
	return(['ip', 'ip']);
}
'''

rec.mods.add('ip', fxn)
