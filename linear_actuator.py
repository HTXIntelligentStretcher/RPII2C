import i2c.i2c_sender as i2c_sender
import rpi_mqtt.libmqtt as libmqtt
import paho.mqtt.subscribe as subscribe
import json
import time

def on_message(client, userdata, message):
  try:
    print("onmessage", message.payload.decode("utf-8"))
    mapped_cmds = list(i2c_sender.map_to_cmds(userdata, 
      message.payload.decode("utf-8")))
    i2c_sender.sendBytes(int(userdata["slave_addr"], 16), 
      int(userdata["actuation_register"], 16), mapped_cmds)
  except OSError as e:
    print(e)

if __name__ == "__main__":
  json_data = json.load(open("/home/pi/RPII2C/config.json",))["linear_actuator"]
  client = libmqtt.initMQTT("linearActuator")
  client.user_data_set(json_data)
  client.on_message = on_message
  client.subscribe(json_data["actuation_topic"], qos=1)
  client.loop_forever()
