
$(document).ready(function(){
	if(Notification.permission === "granted"){
	  $(".tgl-sw-light + .btn-switch").css("background", "#ffdcb3");
	console.log("hei ighen ")
  }

  
var notificationEvents = ['onclick', 'onshow', 'onerror', 'onclose'];
  $("#light-demo3").click(function(){
	  Notification.requestPermission().then(function(result) {
	    if (result === 'denied') {
	      console.log('Permission wasn\'t granted. Allow a retry.');
	      return;
	    }
	    if (result === 'default') {
	      console.log('The permission request was dismissed.');
	      return;
	    }
		$(".tgl-sw-light + .btn-switch").css("background", "#ffdcb3");
	    // Do something with the granted permission.
	  });
	});	  
});
