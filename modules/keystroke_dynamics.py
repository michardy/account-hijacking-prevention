import bcrypt
import rec
from tornado import gen

def reformat(key):
	"""Re-formats database keys to make MongoDB stop complaining they contain periods"""
	return(key.replace('.', '_'))

@gen.coroutine
def hasher(data, key, headers, salt):
	"""This function provides an initial hasher for collected keyboard flight times."""
	hashed = {}
	for k in data.keys():
		#I know I am a terrible person for using the same salt on all of these.  So I promise I will stop
		hashed[reformat(k)] = bcrypt.hashpw(str(int(data[k]) % 10).encode('utf-8'), salt)
		#only once this feature is implemented
		#issue: security
	return(hashed)

rec.rec.add_hasher('keystroke_dynamics', hasher)

@gen.coroutine
def comparer(ses_hash, usr_hash):
	"""This provides a function to compare initially hashed flight times with doubly hashed stored flight times."""
	total = 0
	for k in usr_hash.keys():
		if k in ses_hash:
			total += (bcrypt.hashpw(ses_hash[k], usr_hash[k]) == usr_hash)
	return(total)

rec.rec.add_comparer('keystroke_dynamics', comparer, 1)

def translator(data):
	"""This provides a function that hashes the flight times a second time with a per user hash."""
	salt = bcrypt.gensalt()
	hashed = {}
	for k in data.keys(): #salt reuse
		hashed[k] = bcrypt.hashpw(data[k], salt) #issue: security
	retunr(hashed)

rec.rec.add_translator('keystroke_dynamics', translator)

# JavaScript data collection function
fxn = '''
var keyDynKeys = [];

function keyDynAverage(arr){
	var tot = 0;
	for (var n = 0; n < arr.length; n++){
		tot += arr[n];
	}
	return(tot/arr.length);
}

function keyDynCB(){
	//sort & calculate diffs
	var measurements = {};
	for (var i = 0; i < keyDynKeys.length; i++){
		if (keyDynKeys[i].length !== 1){
			if (keyDynKeys[i][0][0]+'.'+keyDynKeys[i][1][0] in measurements){
				measurements[keyDynKeys[i][0][0]+'.'+keyDynKeys[i][1][0]].push(keyDynKeys[i][1][1]-keyDynKeys[i][0][1]);
			} else {
				measurements[keyDynKeys[i][0][0]+'.'+keyDynKeys[i][1][0]] = [keyDynKeys[i][1][1]-keyDynKeys[i][0][1]];
			}
		}
	}
	keyDynKeys = [];
	// average the diffs, alphabetize, (& remove outliers?)
	var diffs = {};
	for (var i = 0; i < Object.keys(measurements).length; i++){
		var kc = Object.keys(measurements).sort()[i];
		diffs[kc] = keyDynAverage(measurements[kc]);
	}
	send('keystroke_dynamics', diffs, hijackingPreventionCK, hijackingPreventionSID);
}

function keyDynUP(e){
	keyDynKeys.push([[e.keyCode, Date.now()]])
	if (keyDynKeys.length > 100){
		keyDynCB();
	}
}

function keyDynDW(e){
	if (keyDynKeys.length !== 0){
		keyDynKeys[keyDynKeys.length-1].push([e.keyCode, Date.now()]);
	}
}

function keystroke_dynamics(){
	window.onkeydown = keyDynDW;
	window.onkeyup = keyDynUP;
}
'''

rec.mods.add('keystroke_dynamics', fxn, True)
