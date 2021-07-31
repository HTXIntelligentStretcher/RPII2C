import paho.mqtt.client as mqtt #import the client1
import json

def initMQTT(name):
  json_data = json.load(open("./config.json",))["mqtt_server_details"]
  broker_address = json_data["ip"]
  client = mqtt.Client(name) #create new instance
  client.connect(broker_address) #connect to broker
  return client