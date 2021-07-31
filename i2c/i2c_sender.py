from time import sleep
from Adafruit_PureIO.smbus import SMBus
from Raspberry_Pi_Master_for_ESP32_I2C_SLAVE.unpacker import Unpacker
from Raspberry_Pi_Master_for_ESP32_I2C_SLAVE.packer import Packer
from adafruit_extended_bus import ExtendedI2C as I2C
import math

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

if __name__ == "__main__":
  failure = 0
  success = 0
  bytess = [0x01]
  while True:
    try:
      sendBytes(0x04, 0x01, bytess)
      success += 1
    except (OSError, Exception) as e:
      failure += 1
    finally:
      print("success", success)
      print("failure", failure)
