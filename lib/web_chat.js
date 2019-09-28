function update_message(){
 var req = new XMLHttpRequest();
 var d = new Date();
 var reqURL = '/text?' + d.getTime();
 req.onreadystatechange = function(){
     if(req.readyState == 4){
         if(req.status == 200){
             var msg_div = document.getElementById('msg_div');
             var msgs = req.responseText;
             msg_div.innerHTML = msgs;
         }
     }
 }
 req.open('GET', reqURL, true);
 req.send();
}
setInterval(update_message, 1000);
function send_message(){
 	var message = document.getElementById('message').value;
	var ip_input = document.getElementById('remote_ip').value;
	var req = new XMLHttpRequest(); 
	var d = new Date();
 	var reqURL = '/cgi-bin/chat_util.py?' + d.getTime();
 	var formData = new FormData();
 	formData.append('cmd', 'send_msg');
 	formData.append('msg', message);
	formData.append('remote_ip', ip_input);
 	req.onreadystatechange = function(){
     		if(req.readyState == 4){
         		if(req.status == 200){
             			var msgs = req.responseText;
             			console.log(msgs);
         		}
     		}
 	}

 	req.open('POST', reqURL, true);
 	req.send(formData);
}
$(window).bind('beforeunload', function() { 
     var req = new XMLHttpRequest(); 
     var d = new Date();
     var reqURL = '/cgi-bin/chat_util.py?' + d.getTime();
     var formData = new FormData();
     formData.append('cmd', 'close_chat');
     req.open('POST', reqURL, true);
     req.send(formData);
 })
function unload(){
}

function connect_remote(){
	var ip_input = document.getElementById('remote_ip').value;
	var req = new XMLHttpRequest(); 
	var d = new Date();
     	var reqURL = '/cgi-bin/chat_util.py?' + d.getTime();
     	var formData = new FormData();
     	formData.append('cmd', 'connect_remote');
	formData.append('remote_ip', ip_input);
     	req.open('POST', reqURL, true);
     	req.send(formData);
}
