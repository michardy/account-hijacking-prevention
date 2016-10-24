import bcrypt
import rec

def hasher(data):
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(data.encode('utf-8'), salt))

rec.rec.addHasher('ip', hasher)

def comparer(SID, UID, site):
	ssd = db['sessionData_site-' + site]
	sud = db['userData_site-' + site]
	session = ssd.find_one({'sessionID':SID})
	user = sud.find_one({'userID':UID})
	return(session['data'] == user['data'])

rec.rec.addComparer('ip', comparer, 1)
