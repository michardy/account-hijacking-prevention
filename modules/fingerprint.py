import bcrypt
import hijackingprevention.rec as rec
from tornado import gen

import logging
logger = logging.getLogger(__name__)

@gen.coroutine
def hasher(data, headers, salt):
	"""This function provides an initial hasher for browser fingerprints that uses a sitewide salt."""
	return(bcrypt.hashpw(data.encode('utf-8'), salt))

rec.rec.add_hasher('michardy:fingerprint', hasher)

@gen.coroutine
def comparer(ses_hash, usr_hash):
	"""This provides a function to compare initially hashed fingerprints with doubly hashed stored fingerprints."""
	return(bcrypt.hashpw(ses_hash, usr_hash) == usr_hash)

rec.rec.add_comparer('michardy:fingerprint', comparer, 1)

@gen.coroutine
def translator(data):
	"""This provides a function that hashes the fingerprint a second time with a per user hash."""
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(data, salt))

rec.rec.add_translator('michardy:fingerprint', translator)

#JavaScript data collection function
fxn = '''
function fingerprint(){
	var sr = window.screen.height.toString() + window.screen.width.toString() + window.screen.availHeight.toString() + window.screen.availWidth.toString() + navigator.hardwareConcurrency.toString();
	return(['michardy:fingerprint', sr]);
}
'''

rec.mods.add('michardy:fingerprint', fxn, False)
