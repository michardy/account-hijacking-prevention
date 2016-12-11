function hijackingProtectionUserVerify(sid, uid, target){
	var vf = document.createElement('iframe');
	vf.setAttribute('src', 'localhost:8080/dynamic/ask_usr?sid='+sid+'&ck='+ck);
	target.appendChild(vf);
}
