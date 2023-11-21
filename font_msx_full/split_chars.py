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
        x = self.char_w * int(N % self.chars_in_line)
        y = self.char_h * int(N / self.chars_in_line)
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
                x = x0 + xx
                y = y0 + yy
                if self.pix[x, y] == 255:
                    b1 = b1 | (1 << yy)
                    sb[yy] = sb[yy] + '#'
                else:
                    sb[yy] = sb[yy] + ' '
            b.append(b1)
        ss = ss + sb
        ss.append("*/")
        return b, "\n".join(ss)


def bytes_to_code(b):
    s = ["0x%02x" % i for i in b]
    return ", ".join(s)


f = FONTBITMAP("sys2_0002.png")
fo = open("chars.c", "wt")

# ключ - код в 1251, значение - код в кои8, его ищем в картинке

win2koi = {
    254: 192,
    224: 193,
    225: 194,
    246: 195,
    228: 196,
    229: 197,
    244: 198,
    227: 199,
    245: 200,
    232: 201,
    233: 202,
    234: 203,
    235: 204,
    236: 205,
    237: 206,
    238: 207,
    239: 208,
    255: 209,
    240: 210,
    241: 211,
    242: 212,
    243: 213,
    230: 214,
    226: 215,
    252: 216,
    251: 217,
    231: 218,
    248: 219,
    253: 220,
    249: 221,
    247: 222,
    250: 223,
    222: 224,
    192: 225,
    193: 226,
    214: 227,
    196: 228,
    197: 229,
    212: 230,
    195: 231,
    213: 232,
    200: 233,
    201: 234,
    202: 235,
    203: 236,
    204: 237,
    205: 238,
    206: 239,
    207: 240,
    223: 241,
    208: 242,
    209: 243,
    210: 244,
    211: 245,
    198: 246,
    194: 247,
    220: 248,
    219: 249,
    199: 250,
    216: 251,
    221: 252,
    217: 253,
    215: 254,
    218: 255
}

for i in range(256):
    ii = win2koi[i] if i in win2koi else i

    bb, ss = f.get_bytes_for_symbol(ii)
    str_bytes = bytes_to_code(bb)
    # s = "0x06, " + s + ", // %3d  %02x\n" % (i, i)
    s=f"0x06, {str_bytes}, // {i:3d} {i:02x}\n"
    # fo.write("\n")
    # fo.write(ss)
    # fo.write("\n")
    fo.write(s)

fo.close()
