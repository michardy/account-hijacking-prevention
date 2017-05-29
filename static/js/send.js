function hijackingPreventionSend(id, data, ck, sid){
	var xhttpr = new XMLHttpRequest()
	xhttpr.open("POST", "https://hijackingprevention.com/api/sub_dat")
	xhttpr.send(JSON.stringify({'name':id,'data':data,'ck':ck,'sid':sid}))
}
