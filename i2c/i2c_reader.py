from Adafruit_PureIO.smbus import SMBus  # pip install adafruit-blinka
from Raspberry_Pi_Master_for_ESP32_I2C_SLAVE.packer import Packer
from Raspberry_Pi_Master_for_ESP32_I2C_SLAVE.unpacker import Unpacker
import time


def read_from_rpi_to_esp32(addr, register):
  # change 1 of SMBus(1) to bus number on your RPI
  smbus = SMBus(1)
  # prepare the data
  packed = None
  with Packer() as packer:
    packer.write(register)
    packer.write(0x02)
    packer.end()
    packed = packer.read()

  raw_list = None
  smbus.write_bytes(addr, bytearray(packed))
  time.sleep(0.3)  # wait i2c process the request
  first = smbus.read_byte(addr)
  data_length = smbus.read_byte(addr)
  raw_list = list(smbus.read_bytes(addr, data_length - 2))  # the read_bytes contains the data format: first, length, data, crc8, end bytes
  raw_list.insert(0, data_length)
  raw_list.insert(0, first)
  print(raw_list)

  # let's clean received data
  unpacked = None
  with Unpacker() as unpacker:
      unpacker.write(raw_list)
      unpacked = unpacker.read()
  assert unpacked[0] == register
  return unpacked[1:]


if __name__ == "__main__":
  print(read_from_rpi_to_esp32(0x04, 0x01))