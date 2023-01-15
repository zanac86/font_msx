import os
import sys
from PIL import Image


class FONTBITMAP():
    def __init__(self, fn):
        img = Image.open(fn)
        self.pix = img.load()
        self.W = 96
        self.H = 112
        self.char_w = 6
        self.char_h = 8
        self.chars_in_line = 16

    def print_text(self):
        ss = ["/*"]
        for y in range(self.H):
            s = ['#' if self.pix[x, y] == 255 else ' ' for x in range(self.W)]
            ss.append("".join(s))
        s.append("*/")
        return "\n".join(ss)

    def get_bitmap_start_pos(self, N):
        # N - real code 0..255, return x,y bitmap position
        x = self.char_w*int(N % self.chars_in_line)
        y = self.char_h*int(N/self.chars_in_line)
        return x, y

    # упаковываем в байты по столбцам

    def get_bytes_for_symbol(self, N):
        ss = ["/*"]
        sb = ["" for i in range(self.char_h)]
        x0, y0 = self.get_bitmap_start_pos(N)
        b = []
        for xx in range(self.char_w):
            b1 = 0
            for yy in range(self.char_h):
                x = x0+xx
                y = y0+yy
                if self.pix[x, y] == 255:
                    b1 = b1 | (1 << yy)
                    sb[yy] = sb[yy]+'#'
                else:
                    sb[yy] = sb[yy]+' '
            b.append(b1)
        ss = ss+sb
        ss.append("*/")
        return b, "\n".join(ss)


def bytes_to_code(b):
    s = ["0x%02x" % i for i in b]
    return ", ".join(s)


f = FONTBITMAP("font_msx_koi.png")
fo = open("chars.c", "wt")

win2koi = {254: 192, 224: 193, 225: 194, 246: 195, 228: 196, 229: 197, 244: 198, 227: 199, 245: 200, 232: 201, 233: 202, 234: 203, 235: 204, 236: 205, 237: 206, 238: 207, 239: 208, 255: 209, 240: 210, 241: 211, 242: 212, 243: 213, 230: 214, 226: 215, 252: 216, 251: 217, 231: 218, 248: 219, 253: 220, 249: 221, 247: 222, 250: 223,
           222: 224, 192: 225, 193: 226, 214: 227, 196: 228, 197: 229, 212: 230, 195: 231, 213: 232, 200: 233, 201: 234, 202: 235, 203: 236, 204: 237, 205: 238, 206: 239, 207: 240, 223: 241, 208: 242, 209: 243, 210: 244, 211: 245, 198: 246, 194: 247, 220: 248, 219: 249, 199: 250, 216: 251, 221: 252, 217: 253, 215: 254, 218: 255}
# ключ - код в 1251, значение - код в кои8, его ищем в картинке

#
win2koi = {
    142: 0xc0,
    176: 0xc1,
    177: 0xc2,
    134: 0xc3,
    180: 0xc4,
    181: 0xc5,
    132: 0xc6,
    179: 0xc7,
    133: 0xc8,
    184: 0xc9,
    185: 0xca,
    186: 0xcb,
    187: 0xcc,
    188: 0xcd,
    189: 0xce,
    190: 0xcf,
    191: 0xd0,
    143: 0xd1,
    128: 0xd2,
    129: 0xd3,
    130: 0xd4,
    131: 0xd5,
    182: 0xd6,
    178: 0xd7,
    140: 0xd8,
    139: 0xd9,
    183: 0xda,
    136: 0xdb,
    141: 0xdc,
    137: 0xdd,
    135: 0xde,
    138: 0xdf,
    174: 0xe0,
    144: 0xe1,
    145: 0xe2,
    166: 0xe3,
    148: 0xe4,
    149: 0xe5,
    164: 0xe6,
    147: 0xe7,
    165: 0xe8,
    152: 0xe9,
    153: 0xea,
    154: 0xeb,
    155: 0xec,
    156: 0xed,
    157: 0xee,
    158: 0xef,
    159: 0xf0,
    175: 0xf1,
    160: 0xf2,
    161: 0xf3,
    162: 0xf4,
    163: 0xf5,
    150: 0xf6,
    146: 0xf7,
    172: 0xf8,
    171: 0xf9,
    151: 0xfa,
    168: 0xfb,
    173: 0xfc,
    169: 0xfd,
    167: 0xfe,
    170: 0xff,
}


for i in range(256):
    ii = win2koi[i] if i in win2koi else i

    bb, ss = f.get_bytes_for_symbol(ii)
    s = bytes_to_code(bb)
    s = "0x06, "+s+", // %3d  %02x\n" % (i, i)
    fo.write(ss)
    fo.write("\n")
    fo.write(s)
    fo.write("\n")


fo.close()
