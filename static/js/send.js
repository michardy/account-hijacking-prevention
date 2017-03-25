function send(id, data, ck, sid){
	var xhttpr = new XMLHttpRequest()
	xhttpr.open("POST", "http://localhost:8080/api/sub_dat")
	xhttpr.send(JSON.stringify({'name':id,'data':data,'ck':ck,'sessionID':sid,'site':'test'}))
}
