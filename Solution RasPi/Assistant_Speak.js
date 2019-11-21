/////////////
//VARIABLES//
/////////////
var mqtt = require('mqtt');
const say = require('say');
var client  = mqtt.connect('mqtt://192.168.1.177', { port: 1883 });

var snipsUserName = 'GeneraalAlfa';
var wakeword = 'hermes/hotword/default/detected';
var sessionEnd = 'hermes/dialogueManager/sessionEnded';
var machineState = 'Test/Text_To_Speech';

//////////////
//ON CONNECT//
//////////////
client.on('connect', function() {
   console.log('Connected to Snips MQTT server\n');
   client.subscribe('hermes/hotword/default/detected');
   client.subscribe('hermes/dialogueManager/sessionEnded');
   client.subscribe(machineState);
});

//////////////
//ON MESSAGE//
//////////////
client.on('message', function(topic,message) {
   //var message = JSON.parse(message);
   //console.log('Commando: ' + message);
   //console.log('Commando: ' + topic);

   switch(topic) {
       // * On Wakeword
       case wakeword:
           console.log('Wakeword Detected');
       break;
       // * On MachineState
       case machineState:
           try{
				// * {"text": "This is a test"}
				obj = JSON.parse(message);
				commando = obj.text;
				say.speak(commando);
                console.log('Commando: ' + commando);
           }
           catch(e){
               console.log('No valid command');
           }
       break;
       // * On Conversation End
       case sessionEnd:
           console.log('Session Ended\n');
       break;
   }
});