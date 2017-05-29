function hijackingProtectionUserVerify(sid, target){
	var vf = document.createElement('iframe');
	vf.setAttribute('src', 'https://hijackingprevention.com/dynamic/ask_usr?sid='+sid+'&ck='+ck);
	target.appendChild(vf);
}
