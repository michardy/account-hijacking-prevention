import bcrypt
import hijackingprevention.rec as rec
from tornado import gen

import logging
logger = logging.getLogger(__name__)

@gen.coroutine
def hasher(data, headers, salt):
	"""This function provides a hasher for received IP adresses that hashes with an intial sitewide salt."""
	ip = headers.get('X-Real-IP')
	return(bcrypt.hashpw(ip.encode('utf-8'), salt))

rec.rec.add_hasher('michardy:ip', hasher) #register the previous function

@gen.coroutine
def comparer(ses_hash, usr_hash):
	"""This function provides a means of comparing per user hashed IP addresses with session address hashes."""
	return(bcrypt.hashpw(ses_hash, usr_hash) == usr_hash)

rec.rec.add_comparer('michardy:ip', comparer, 1) #register the previous function

@gen.coroutine
def translator(data):
	"""This function provides a second stage per user salted hasher for data that will be stored indefinitly."""
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(data, salt))

rec.rec.add_translator('michardy:ip', translator) #register previous function

#JavaScript data collection function
#In this case the data is pulled from headers so we just need a request 
fxn = '''
function ip(){
	return(['michardy:ip', 'ip']);
}
'''

rec.mods.add('michardy:ip', fxn, False)
