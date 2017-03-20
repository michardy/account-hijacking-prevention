import rec

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
	console.log(diffs);
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
