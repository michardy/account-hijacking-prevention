import rec

fxn = '''
var keys = [];

function keyDynCB(){
	//copy var
	//clear var
	//loop through and average
	//reschedule
}

function keyDynUP(e){
	keys.push([[e.keyCode, Date.now()]])
}

function keyDynDW(e){
	keys[keys.length()-1].push([e.keyCode, Date.now()])
}

function keyDyn(){
	window.onkeydown = keyDynDW(e)
	window.onkeyup = keyDynUUP(e)
	//reg callback
}
'''

rec.mods.add('fingerprint', fxn)
