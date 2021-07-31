import i2c.i2c_reader as i2c_reader
import rpi_mqtt.libmqtt as libmqtt
import json
import time
import struct


def periodicallyRead(topic, slave_addr, register):
  
  failures=0
  sucess=0
  while True:
    try:
      weightt = i2c_reader.read_from_rpi_to_esp32(slave_addr, register)
      weight = struct.unpack('>f', weightt)[0]
      print("weight2", weight)
      client.publish(topic, json.dumps({'weight': weight}))
      time.sleep(0.05)
      sucess+=1
    except (OSError, Exception) as e:
      print("failed")
      failures+=1
    finally:
      print("successes", sucess)
      print("failures", failures)

if __name__ == "__main__":
  client = libmqtt.initMQTT("weight")
  json_data = json.load(open("./config.json",))["weight_sensor"]
  # periodicallyRead(json_data["weight_topic"], int(json_data["slave_addr"], 16), int(json_data["weight_register"], 16))
  periodicallyRead(json_data["weight_topic"], 0x06, int(json_data["weight_register"], 16))

