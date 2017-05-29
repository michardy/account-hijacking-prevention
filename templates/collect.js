{% for c in collectors %}
{% raw c %}
{% end %}

var collectors = {% raw col_list %};
var async = {% raw async_list %}

function hijackingPreventionCollect(){
	for (var c = 0; c < collectors.length; c++){
		var res = eval(collectors[c]+'()');
		if (!async[c]){
			hijackingPreventionSend(res[0], res[1], hijackingPreventionCK, hijackingPreventionSID);
		}
	}
}

hijackingPreventionCollect();
