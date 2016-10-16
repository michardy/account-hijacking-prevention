{{ collectors }}

var collectors = {{ colList  }};

function collect(){
	for (var c = 0; i < collectors.length; c++;){
		collectors[c]();
	}
	send();
}
