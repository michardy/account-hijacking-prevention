import bcrypt
import rec
import api_user
from tornado import gen

import logging
logger = logging.getLogger(__name__)

@gen.coroutine
def hasher(data, key, headers, db):
	"""This function provides a hasher for received IP adresses that hashes with an intial sitewide salt."""
	site = api_user.Site(db)
	yield site.get_by_client_key(key, headers.get('Host'))
	salt = site.get_salt('ip')
	ip = headers.get('X-Real-IP')
	return(bcrypt.hashpw(ip.encode('utf-8'), salt))

rec.rec.add_hasher('ip', hasher) #register the previous function

def comparer(ses_hash, usr_hash, site, db):
	"""This function provides a means of comparing per user hashed IP addresses with session address hashes."""
	try:
		if bcrypt.hashpw(ses_hash, usr_hash) == usr_hash:
			return(True)
		return(False)
	except KeyError:
		logger.error('User session data expired')
		return(0)

rec.rec.add_comparer('ip', comparer, 1) #register the previous function

def translator(data):
	"""This function provides a second stage per user salted hasher for data that will be stored indefinitly."""
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(data.encode('utf-8'), salt))

rec.rec.add_translator('ip', translator) #register previous function

#JavaScript data collection function
#In this case the data is pulled from headers so we just need a request 
fxn = '''
function ip(){
	return(['ip', 'ip']);
}
'''

rec.mods.add('ip', fxn)
