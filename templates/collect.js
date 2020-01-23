{% for c in collectors %}
{% raw c %}
{% end %}

var collectors = {% raw col_list %};
var callback = {% raw callback_list %}

function hijackingPreventionCollect(){
	for (var c = 0; c < collectors.length; c++){
		var res = eval(collectors[c]+'()');
		if (!callback[c]){
			hijackingPreventionSend(res[0], res[1], hijackingPreventionCK, hijackingPreventionSID);
		}
	}
}

hijackingPreventionCollect();
