import i2c.i2c_sender as i2c_sender
import rpi_mqtt.libmqtt as libmqtt
import paho.mqtt.subscribe as subscribe
import json
import time

def on_message(client, userdata, message):
  try:
    i2c_sender.sendBytes(userdata["slave_addr"], userdata["actuation_register"], message.payload)
  except e:
    pass

if __name__ == "__main__":
  json_data = json.load(open("./config.json",))["linear_actuator"]
  client = libmqtt.initMQTT("linearActuator")
  client.user_data_set(json_data)
  client.on_message = on_message
  client.subscribe(json_data["actuation_topic"], qos=1)
