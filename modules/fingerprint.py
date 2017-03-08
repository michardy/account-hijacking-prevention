import bcrypt
import rec
import hashlib
import api_user
from tornado import gen

import logging
logger = logging.getLogger(__name__)

@gen.coroutine
def hasher(data, key, headers, db):
	"""This function provides an initial hasher for browser fingerprints that uses a sitewide salt."""
	site = api_user.Site(db)
	yield site.get_by_client_key(key, headers.get('Host'))
	salt = site.get_salt('fingerprint')
	return(hashlib.sha512(data.encode('utf-8') + salt).hexdigest())

rec.rec.add_hasher('fingerprint', hasher)

@gen.coroutine
def comparer(session, user, site, db):
	"""This provides a function to compare initially hashed fingerprints with doubly hashed stored fingerprints."""
	try:
		for h in user['fingerprint']:
			if bcrypt.hashpw(session['fingerprint'].encode('utf-8'), h) == h:
				return(True)
		return(False)
	except KeyError:
		logger.error('User session data expired')
		return(0)

rec.rec.add_comparer('fingerprint', comparer, 1)

def translator(data):
	"""This provides a function that hashes the fingerprint a second time with a per user hash."""
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(data.encode('utf-8'), salt))

rec.rec.add_translator('fingerprint', translator)

#JavaScript data collection function
fxn = '''
function fingerprint(){
	var sr = window.screen.height.toString() + window.screen.width.toString() + window.screen.availHeight.toString() + window.screen.availWidth.toString();
	return(['fingerprint', sr]);
}
'''

rec.mods.add('fingerprint', fxn)
