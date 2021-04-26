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
        for y in range(self.H):
            s = ['#' if self.pix[x, y] == 255 else ' ' for x in range(self.W)]
            print("".join(s))

    def get_bitmap_start_pos(self, N):
        # N - real code 0..255, return x,y bitmap position
        x = self.char_w*int(N % self.chars_in_line)
        y = self.char_h*int(N/self.chars_in_line)
        return x, y

    def get_bytes_for_symbol(self, N):
        x0, y0 = self.get_bitmap_start_pos(N)
        b = []
        for xx in range(self.char_w):
            b1 = 0
            for yy in range(self.char_h):
                x = x0+xx
                y = y0+yy
                if self.pix[x, y] == 255:
                    b1 = b1 | (1 << yy)
            b.append(b1)
        return b


def bytes_to_code(b):
    s = ["0x%02x" % i for i in b]
    return ", ".join(s)


f = FONTBITMAP("font_msx_koi.png")
f.print_text()

fo = open("font_msx.c", "wt")

for i in range(32, 128):
    s = bytes_to_code(f.get_bytes_for_symbol(i))
    s = "0x06, "+s+", // %3d %c\n" % (i, i)
    fo.write(s)

fo.close()


'''
размер символа 6х8

кодировка на картинке кои-8
символы 32..127 переводим напрямую
символы 128-191 псевдографика нафиг
символы 192-255 русские по таблице koi2win

Конвертируем с 32 до 127

Чтобы русский текст набирать на клавиатуре в англ раскладке,
а в шрифте они будут реально русские

ABCDEFGHIJKLMNOPQRSTUVWXYZ{}:"<>
ФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯХЪЖЭБЮ

abcdefghijklmnopqrstuvwxyz[];',.
фисвуапршолдьтщзйкыегмцчняхъжэбю

для кода 0x41='A'eng надо взять код 0xD4='Ф'rus
код 0xD4 перевести в КОИ8 и найти начальный адрес битмапа на картинке

'''
