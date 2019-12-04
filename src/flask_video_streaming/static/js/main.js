 	
    var socket = io.connect('http://192.168.43.202:5000');
    // var socket = io.connect('http://192.168.43.150:5000');
    	socket.on('after_connect', function(msg){
   			console.log('After connect: ', msg.data);
			});

    	socket.on('update value', function(msg){
    		console.log('value updated')
    		document.getElementById('speedText').innerHTML ="speed: "+Math.floor(msg.vel*100)/100;
        document.getElementById('omegaText').innerHTML ="omega: "+Math.floor(msg.omega*100)/100;
    	});

 
    	var iv;
    	function vPlus_down(){
    	iv = setInterval(()=>sync(v=.2,w=0,stop=false),200);
    	}
    	function vMinus_down(){
    	iv = setInterval(()=>sync(v=-.2,w=0,stop=false),200);
    	}
    	function wPlus_down(){
    	iv = setInterval(()=>sync(v=0,w=.1,stop=false),200);
    	}
    	function wMinus_down(){
    	iv = setInterval(()=>sync(v=0,w=-.1,stop=false),200);
    	}
      function stop_down(){
      iv = setInterval(()=>sync(v=0,w=0,stop=true),200);
      }
    	
    	function up(){
    		clearInterval(iv);
    		console.log("up()")
    	}

    	function sync(v=0,w=0,stop=false){
    	// var sv1 = document.getElementById("slider1").value;
        console.log(v,w,stop);
        if(stop==true){
              socket.emit('value changed', 0);
        }else{
	var msgs={
		vel:v,
		omega:w,
	};
    	// document.getElementById('txt').innerHTML=sv1.toString();

        socket.emit('value changed', msgs);
        }
    	}




var elem = document.body;

/* Function to open fullscreen mode */
function openFullscreen() {
var elem = document.body;
  /* If fullscreen mode is available, show the element in fullscreen */
  if (
    document.fullscreenEnabled || /* Standard syntax */
    document.webkitFullscreenEnabled || /* Chrome, Safari & Opera */
    document.mozFullScreenEnabled || /* Firefox */
    document.msFullscreenEnabled /* IE/Edge */
  ) {
   
    /* Show the element in fullscreen */
    elem.webkitRequestFullscreen();
    if (elem.requestFullscreen) {
      elem.requestFullscreen(); /* Standard syntax */
    } else if (elem.mozRequestFullScreen) { /* Firefox */
      elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
      elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE/Edge */
      elem.msRequestFullscreen();
    }
    
  }
}

//openFullscreen();

