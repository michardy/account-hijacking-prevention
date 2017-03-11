import bcrypt
import rec
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
	return(bcrypt.hashpw(data.encode('utf-8'), salt))

rec.rec.add_hasher('fingerprint', hasher)

@gen.coroutine
def comparer(ses_hash, usr_hash, site, db):
	"""This provides a function to compare initially hashed fingerprints with doubly hashed stored fingerprints."""
	return(bcrypt.hashpw(ses_hash, usr_hash) == usr_hash)

rec.rec.add_comparer('fingerprint', comparer, 1)

def translator(data):
	"""This provides a function that hashes the fingerprint a second time with a per user hash."""
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(data, salt))

rec.rec.add_translator('fingerprint', translator)

#JavaScript data collection function
fxn = '''
function fingerprint(){
	var sr = window.screen.height.toString() + window.screen.width.toString() + window.screen.availHeight.toString() + window.screen.availWidth.toString() + navigator.hardwareConcurrency.toString();
	return(['fingerprint', sr]);
}
'''

rec.mods.add('fingerprint', fxn)
