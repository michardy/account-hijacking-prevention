function hijackingProtectionUserVerify(sid, target){
	var vf = document.createElement('iframe');
	vf.setAttribute('src', 'http://localhost:8080/dynamic/ask_usr?sid='+sid+'&ck='+ck);
	target.appendChild(vf);
}
