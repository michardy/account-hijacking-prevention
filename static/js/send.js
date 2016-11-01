function send(id, data, ck, sid){
	console.log({id, data, ck, sid});
	var xhttpr = new XMLHttpRequest()
	xhttpr.oreadystatechange = function (){
		if (this.status == 200){
			alert('ran');
		}
	}
	xhttpr.open("POST", "http://localhost:8080/api/sub_dat")
	//xhttpr.send('name='+id+'&data='+data+'&ck='+ck+'&sessionID='+sid+'&site=test')
	xhttpr.send(JSON.stringify({'name':id,'data':data,'ck':ck,'sessionID':sid,'site':'test'}))
}
