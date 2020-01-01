import paho.mqtt.client as mqtt
import json

#broker_url = "192.168.1.174"
broker_url = "192.168.0.115"
broker_port = 1883

def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code "+rc)

def on_disconnect(client, userdata, rc):
   print("Client Got Disconnected")

def on_message(client, userdata, message):
   #print("Message Recieved: "+message.payload.decode())
   test=json.loads(message.payload.decode())
   print(test["input"])

   if test["input"].lower() == "take picture":
       # Set code here
       print("test 1")
   else if test["input"].lower() == "scan":
       # Set code here
       print("test 2")
   else if test["input"].lower() == "scan difference":
       # Set code here
       print("test 3")
   else if test["input"].lower() == "outline":
       # Set code here
       print("test 4")
   else if test["input"].lower() == "create g-code":
       # Set code here
       print("test 5")
   else if test["input"].lower() == "object detect":
       # Set code here
       print("test 6")
   else if test["input"].lower() == "find angle and centre point":
       # Set code here
       print("test 7")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)

#client.subscribe("TestingTopic", qos=1)
client.subscribe("hermes/intent/GeneraalAlfa:Vision", qos=1)

#client.publish(topic="TestingTopic", payload="TestingPayload", qos=1, retain=False)
client.publish(topic="Test/Text_To_Speech", payload='{"text": "dit is een test"}', qos=1, retain=False)

client.loop_forever()
