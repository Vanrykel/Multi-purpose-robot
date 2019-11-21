import paho.mqtt.client as mqtt

broker_url = "192.168.1.174"
broker_port = 1883

def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code "+rc)

def on_disconnect(client, userdata, rc):
   print("Client Got Disconnected")

def on_message(client, userdata, message):
   print("Message Recieved: "+message.payload.decode())
   test=message.payload.decode()
   
   for sleutel in test.keys():
      if sleutel == 'input':
         result = test[sleutel]
         print(result)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)

client.subscribe("TestingTopic", qos=1)

client.publish(topic="TestingTopic", payload="TestingPayload", qos=1, retain=False)

client.loop_forever()
