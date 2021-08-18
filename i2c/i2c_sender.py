from time import sleep
from Adafruit_PureIO.smbus import SMBus
from Raspberry_Pi_Master_for_ESP32_I2C_SLAVE.unpacker import Unpacker
from Raspberry_Pi_Master_for_ESP32_I2C_SLAVE.packer import Packer
from adafruit_extended_bus import ExtendedI2C as I2C
import math
import json

def sendBytes(addr, registerCode, bytess):
  max_packet_length = 124
  # i2c = I2C(1)
  # scan = i2c.scan()
  # print("I2c devices found: ", scan)
  with SMBus(1) as smbus:
    # address = scan[0]
    print(f"byte length: {len(bytess)}")
    if len(bytess) == 0:
      return
    if len(bytess) > max_packet_length:
      print("Too many bytes")
      return
    with Packer() as packer:
      packer.debug = True
      packer.write(registerCode)
      packer.write(0x01)
      for b in bytess:
        packer.write(b)
      packer.end()
      packed = packer.read()
      # print("packed: ", packed)
      smbus.write_bytes(addr, bytearray(packed))
      print("Bytes written")

def map_to_cmds(userdata, payload):
  given_cmds = json.loads(payload)
  for given_cmd in given_cmds.items():
    if given_cmd[0] not in userdata["cmd_mapping"].keys():
      yield 0x00
    for cmd_type in userdata["cmd_mapping"][given_cmd[0]].items():
      if cmd_type[0] == given_cmd[1]:
        yield int(cmd_type[1], 16)

if __name__ == "__main__":
  failure = 0
  success = 0
  bytess = [0x01]
  while True:
    try:
      sendBytes(0x06, 0x01, bytess)
      success += 1
    except (OSError, Exception) as e:
      failure += 1
    finally:
      print("success", success)
      print("failure", failure)
