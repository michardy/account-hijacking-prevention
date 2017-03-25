function hijackingProtectionUserVerify(sid, target){
	var vf = document.createElement('iframe');
	vf.setAttribute('src', 'http://54.202.247.3/dynamic/ask_usr?sid='+sid+'&ck='+ck);
	target.appendChild(vf);
}
