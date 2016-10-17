import api
import bcrypt
import hashlib

def hasher(data):
	initialH = hashlib.sha256(data)
	salt = bcrypt.gensalt()
	return(bcrypt.hashpw(initialH, salt))

api.addHasher('ip', hasher)

def comparer(hash, hash):
	return(hash == hash)

api.addComparer('ip', comparer)
