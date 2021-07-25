from time import sleep
from Adafruit_PureIO.smbus import SMBus
from Raspberry_Pi_Master_for_ESP32_I2C_SLAVE.unpacker import Unpacker
from Raspberry_Pi_Master_for_ESP32_I2C_SLAVE.packer import Packer
from adafruit_extended_bus import ExtendedI2C as I2C

def sendBytes(addr, bytess):
  max_packet_length = 124
  # i2c = I2C(1)
  # scan = i2c.scan()
  # print("I2c devices found: ", scan)
  with SMBus(1) as smbus:
    # address = scan[0]
    print(f"byte length: {len(bytess)}")
    if len(bytess) == 0:
      return
    counter = 0
    with Packer() as packer:
      packet_num = (int(len(bytess) / max_packet_length)) + 1
      packer.debug = True
      packer.write(0x00)
      packer.write(packet_num)
      packer.end()
      packed = packer.read()
      smbus.write_bytes(addr, bytearray(packed))
    while counter < len(bytess):
      with Packer() as packer:
        packer.debug = False
        packer.write(bytess[counter])
        counter += 1
        while counter % max_packet_length != 0 and counter < len(bytess):
          packer.write(bytess[counter])
          counter += 1
        packer.end()
        packed = packer.read()
        # print("packed: ", packed)
      smbus.write_bytes(addr, bytearray(packed))

bytess = bytearray("""We, the citizens of Singapore,
pledge ourselves as one united people,
regardless of race, language or religion,
to build a democratic society
based on justice and equality
so as to achieve happiness, prosperity
and progress for our nation.""", "utf8")

sendBytes(0x04, bytess)