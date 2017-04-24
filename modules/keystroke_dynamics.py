import bcrypt
import hijackingprevention.rec as rec
from tornado import gen
#from cryptography.fernet import Fernet

def reformat(key):
	"""Re-formats database keys to make MongoDB stop complaining they contain periods"""
	return(key.replace('.', '_'))

@gen.coroutine
def hasher(data, headers, salt):
	"""This function provides an initial hasher for collected keyboard flight times."""
	hashed = {}
	for k in data.keys():
		#I know I am a terrible person for not hashing
		hashed[reformat(k)] = data[k]
		#But I am not sure how to hash the data so that I can do math with it later
		#issue: security
	return(hashed)

rec.rec.add_hasher('keystroke_dynamics', hasher)

@gen.coroutine
def comparer(ses_hash, usr_hash):
	"""This provides a function to compare initially hashed flight times with doubly hashed stored flight times."""
	total = 0
	kmax = 0
	for k in usr_hash.keys():
		if k in ses_hash:
			kmax += 1
			total += (abs(int(ses_hash[k]) - int(usr_hash[k])) - 24)
	score = 4.8 - (total/kmax) #4 ms minus average deviation off normal
	if score > 4.8:
		score = 1
	elif score < 0:
		score = 0
	else:
		score = abs(score)/4.8
	return(score)

rec.rec.add_comparer('keystroke_dynamics', comparer, 1)

@gen.coroutine
def translator(data):
	"""This provides a function that hashes the flight times a second time with a per user hash."""
	#hashed = {}
	#for k in data.keys(): #no hashing
		#maybe encrypt db keys to anonymize data
		#hashed[k] = data[k] #issue: security
	return(data)

rec.rec.add_translator('keystroke_dynamics', translator)

# JavaScript data collection function
fxn = '''
var keyDynKeys = [];

function keyDynAverage(arr){
	var tot = 0;
	var valPoints = 0;
	for (var n = 0; n < arr.length; n++){
		if (arr[n] < 100){
			valPoints += 1;
			tot += arr[n];
		}
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
	hijackingPreventionSend('keystroke_dynamics', diffs, hijackingPreventionCK, hijackingPreventionSID);
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
	document.addEventListener('keydown', keyDynDW, false);
	document.addEventListener('keyup', keyDynUP, false);
}
'''

rec.mods.add('keystroke_dynamics', fxn, True)
