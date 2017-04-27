// A small script to change the color of the notification permission button
$(document).ready(function(){
	// if the browser already has permitted our webpage to allow use of notification it should change the color of the button on page load.
	if(Notification.permission === "granted"){
	  $(".tgl-sw-light + .btn-switch").css("background", "#ffdcb3");
	console.log("hei ighen ")
  }

// if the browser hadn't already given permission to allow notification you have to click the permission button  
var notificationEvents = ['onclick', 'onshow', 'onerror', 'onclose'];
  $("#light-demo3").click(function(){
	  Notification.requestPermission().then(function(result) {
		  // If the permission button was not granted it should allow it should just return.
	    if (result === 'denied') {
	      console.log('Permission wasn\'t granted');
	      return;
	    }
		// if the permission dialog was not answered but just closed it should do nothing.
	    if (result === 'default') {
	      console.log('The permission request was dismissed.');
	      return;
	    }
		// If none of the earlier if-sentences are true it, the permission were accepted and the color of the button should change.
		$(".tgl-sw-light + .btn-switch").css("background", "#ffdcb3");
	    // Do something with the granted permission.
	  });
	});	  
});
