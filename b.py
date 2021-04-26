import os
import sys
import struct

bb = [i for i in range(256)]
bb[127]=32
b = bb

print(len(b))
s = struct.pack("="+"B"*len(b), *b)

f = open("bytes.bin", "wb")
f.write(s)
f.close()
