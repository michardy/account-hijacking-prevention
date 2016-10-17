import bcrypt
import hashlib
import modules

def hasher(data):
	initialH = hashlib.sha256(data)
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(initialH, salt))

modules.receiver.rec.addHasher('ip', hasher)

def comparer(SID, UID, site):
	ssd = db['sessionData_site-' + site]
	sud = db['userData_site-' + site]
	session = ssd.find_one({'sessionID':SID})
	user = sud.find_one({'userID':UID})
	return(session['data'] == user['data'])

modules.receiver.api.addComparer('ip', comparer)
