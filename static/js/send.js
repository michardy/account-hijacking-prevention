function send(id, data, ck, sid){
	var xhttpr = new XMLHttpRequest()
	xhttpr.open("POST", "http://54.202.247.3/api/sub_dat")
	xhttpr.send(JSON.stringify({'name':id,'data':data,'ck':ck,'sessionID':sid,'site':'test'}))
}
