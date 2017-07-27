function list() {
	showdown.setFlavor('github');
	var conv = new showdown.Converter();
	var b = document.getElementById('board');
	var p = JSON.parse(this.responseText);
	for (r in p) {
		var text = p[r]['body'].substring(
			p[r]['body'].lastIndexOf("[//]: # (START MITIGATION)\r\n\r\n")+30,
			p[r]['body'].lastIndexOf("\r\n\r\n[//]: # (END MITIGATION)")
		);
		var html = conv.makeHtml(text);
		b.innerHTML += '<tr><td class="outer"><table><tr><th><a href="' + p[r]['html_url'] + '">' + p[r]['title'] + '</a></th></tr><tr><td>'+html+'</td></tr></table</td></tr>';
	}
}

var xmlHTTP = new XMLHttpRequest();
xmlHTTP.addEventListener('load', list);
xmlHTTP.open('GET', 'https://api.github.com/repos/michardy/account-hijacking-prevention/issues?labels=security,bug');
xmlHTTP.send();
