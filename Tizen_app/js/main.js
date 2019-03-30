window.onload = function () {
    // TODO:: Do your initialization job
	
	//	initialize bluetooth adapter
	
	var adapter = tizen.bluetooth.getLEAdapter();
//	serviceuuids: ['180f'] /* 180F is 16bit Battery Service UUID */
//	var advertiseData = new tizen.BluetoothLEAdvertiseData({
//	    includeName: true,
//	    
//		serviceuuids: ["0bd51666-e7cb-469b-8e4d-2742f1ba77cc"]  /* 180F is 16bit Battery Service UUID   */
//	});
	
	
	var advertiseData = new tizen.BluetoothLEAdvertiseData({
		     includeName: true,          // Whether the device name should be included
		     includeTxPowerLevel: true,    // Whether the transmission power level should be included
			 uuids: ['18031993-1234-abcd-0000-222222222222']
		 });
	
	var connectable = false;
	
    // add eventListener for tizenhwkey
    document.addEventListener('tizenhwkey', function(e) {
        if(e.keyName == "back")
	try {
	    tizen.application.getCurrentApplication().exit();
	} catch (ignore) {
	}
    });
    
 // sleep time expects milliseconds
    function sleep (time) {
      return new Promise((resolve) => setTimeout(resolve, time));
    }

    // Sample code
    var textbox = document.querySelector('.contents');
    textbox.addEventListener("click", function(){
    	box = document.querySelector('#textbox');
    	if(box.innerHTML == "Beacon"){
    		adapter.startAdvertise(advertiseData, 'ADVERTISE', function onstate(state) {
    		    console.log('Advertising configured: ' + state);
    		}, function(error) {
    		    console.log('startAdvertise() failed: ' + error.message);
    		}, 'LOW_LATENCY', connectable);
    		box.innerHTML = 'STOP';
    		document.getElementsByTagName("body")[0].style = 'background-color:red';
    	    // Usage!
    	    sleep(600).then(() => {
    	    	console.log('zabijimadvertise');
        		adapter.stopAdvertise();
        		box.innerHTML = 'Beacon';
        		document.getElementsByTagName("body")[0].style = 'background-color:green';
    	    });
    	}else{
    		console.log('zabijimadvertise');
    		adapter.stopAdvertise();
    		box.innerHTML = 'Beacon';
    		document.getElementsByTagName("body")[0].style = 'background-color:green';
    	}
    	
    });
    
};
