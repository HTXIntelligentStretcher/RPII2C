import struct
a = bytearray([62, 148, 122, 225])
print(a)
b = struct.unpack('f', a)
print(b)