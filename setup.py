from pymongo import MongoClient
import hijackingprevention.rec as rec
import config
import bcrypt
import secrets


client = MongoClient()
db = client.hijackingPrevention
sl = db.siteList

cont = True
while cont:
	host = input('Host: ')
	ck = secrets.token_urlsafe(64)
	ak = secrets.token_urlsafe(64)
	salts = {}
	for i in rec.mods.fxn_names:
		salts[i] = bcrypt.gensalt()
	site = {'host':host, 'clientKey':ck, 'serverKey':ak, 'salts':salts}
	sl.insert_one(site)
	cont = input('Add another site? y/n: ').lower().startswith('y')
