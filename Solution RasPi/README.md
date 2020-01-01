# TEXT-TO-SPEECH

## SNIPS TEXT-TO-SPEECH
While Snips (.ai) is a speech-to-text program/application, it also has a text-to-speech application integrated. This makes it possible for the various programs and applications to indicate if an error has occurred or what objects have been detected. In order to use the text-to-speech of Snips (.ai) a message has to be send over MQTT. The message has to be of the form:
- '{"init":{"type":"notification","text":"hello world"}}'
Most of the parameters are already set correctly, only the value of "text" must be changed with the text that must be spoken. In the example above, the values is set as "hello world".
Another important parameter is the topic the message will be sent to MQTT. The specific topic, to use the text-to-speech is 
- 'hermes/dialogueManager/startSession'.
But there is one mayer disadvantage of this text-to-speech and that is that the sounds it produces of very low quality is. The speech it produces is unintelligible and contains a lot of noise. Which makes it unusable.

## ALTERNATIVE TEXT-TO-SPEECH
Because of the low quality of the Snips text-to-speech, an alternative was used: Say.js. In contrast to Snips text-to-speech, the Say.js text-to-speech is of higher quality when it comes to its speech. The speech is fluent and does not contain any noise.
In order to use say.js a NodeJS program had to been made in order to receive messages over MQTT. This gives it more flexibility and makes it possible to add extra functionalities.
There are two topics the application is listening to for messages:
- 'Test/Text_To_Speech'
- 'hermes/intent/GeneraalAlfa:Show_commands'
The first topic is used by the different applications and programs of the project. The messages that are expected to be received are Json messege of the form: ‘{"text": "This is a test"}’. The NodeJS program takes the value of “text” and convert it to speech.
The second topic is used to receive specific commands from Snips. The Snips assistant has been configured to only send one command over this topic, namely: “show commands”. This is send as a json message. When this message is received a list of the different commands of the hole project will be summeriased. This is done inorder to let new user now what the different commands are.

#Vision 

This are programs for objectdetection and outling using a camra and using the information we get on a cartethic robot. 

##description 

The vision part is written in Python there is the python code what you can run on the raspberry Pi and .ipynb those are Jupiter Notbook files also written in python.
In the Jupiter Notbook files, it is easier to visualize all the steps and you can see what happens step by step.
We got three files that we must run. The scan file is executed first Here we take a picture of the object.
Then we can run the object detection file and the FTP file or the outline file and the G-code converter.
In the object detection file we detect the items and get there rotated angles of the items the four corner coordinates and the centre of the items.
We send this information in JSON format to the PLC using FTP.
In the outline file the outline of all the items will be taken and will be converted to G-code by using the G-code converter.
You can see a flowchart of the process in the photo flowchart program. 

 ![flowchart program](/flowchart.png)