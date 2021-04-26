# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog


START = """#ifndef FONT5X7_H
#define FONT5X7_H

#ifdef __AVR__
 #include <avr/io.h>
 #include <avr/pgmspace.h>
#else
 #define PROGMEM
#endif

// Standard ASCII 5x7 font

static const unsigned char font[] PROGMEM = {
"""
END = """};
#endif // FONT5X7_H"""


def hexf(x):
    return hex(x)[2:].upper().rjust(2, "0")


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        m = Menu(self)
        m.add_command(label="Open", command=self.open_file)
        m.add_command(label="Save", command=self.save_file)
        master.config(menu=m)
        self.canvas = Canvas(self, width=464, height=408, highlightthickness=0)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.pack(padx=5, pady=5)
        self.area = []
        for x in range(5):
            for y in range(8):
                self.area.append(self.canvas.create_rectangle(
                    x * 51, y * 51, x * 51 + 50, y * 51 + 50, fill="white", width=0))
        self.indexs, self.images, self.rectangles = [], [], []
        image = PhotoImage(width=10, height=16)
        for y in range(16):
            for x in range(10):
                image.put("#fff", (x, y))
        for y in range(1, 17, 1):
            for x in range(1, 17, 1):
                i = 0 if y < 9 else 1
                self.rectangles.append(self.canvas.create_rectangle(
                    x * 12 + 260, y * 18 + i, x * 12 + 271, y * 18 + i + 17, fill="white", outline="grey"))
                img = image.copy()
                self.indexs.append(self.canvas.create_image(
                    x * 12 + 261, y * 18 + i + 1, image=img, anchor=NW))
                self.images.append(img)
        for xy in range(1, 17, 1):
            i = 0 if xy < 9 else 1
            self.canvas.create_text(
                xy * 12 + 266, 10, text=hex(xy - 1)[2:].upper())
            self.canvas.create_text(
                266, xy * 18 + i + 8, text=hex(xy - 1)[2:].upper())
        self.canvas.create_line(260, 162, 464, 162, fill="red")
        self.canvas.create_text(270, 330, text="Selected int:", anchor=SW)
        self.canvas.create_text(345, 330, text=" ", anchor=SW, tags="INT")
        self.canvas.create_text(270, 350, text="Selected hex:", anchor=SW)
        self.canvas.create_text(345, 350, text=" ", anchor=SW, tags="HEX")
        self.index = 0
        self.load(self.images[self.index])
        self.canvas.itemconfig(self.rectangles[self.index], outline="blue")

    def open_file(self):
        filename = filedialog.askopenfilename(defaultextension='.c', filetypes=[
            ('all files', '.*'), ('c code', '.c')])
        if not filename:
            return
        try:
            txt = open(filename, "rt").read()
        except:
            print("cannot open file")
            return
        start = txt.find("{")
        if start == -1:
            print("cannot find array start")
            return
        end = txt.find("}", start)
        if end == -1:
            print("cannot find array end")
            return
        txt = txt[start:end + 1]
        txt = txt.replace("{", "[")
        txt = txt.replace("}", "]")
        txt = txt.replace("//", "#")
        try:
            sp = eval(txt)
        except:
            print("wrong array format")
            return
        if len(sp) != 1280:
            print("wrong array length, try: 256 rows by 5 columns, total 1280 elements")
            return
        for i in range(256):
            txt = []
            for b in sp[i * 5:i * 5 + 5]:
                txt += list(bin(b)[2:].rjust(8, "0")[::-1])
            image = self.images[i]
            for x in range(5):
                for y in range(8):
                    color = "#fff" if txt.pop(0) == "0" else "#000"
                    self.putpixel(image, x, y, color)
        self.canvas.itemconfig(self.rectangles[self.index], outline="grey")
        self.index = 0
        self.load(self.images[self.index])
        self.canvas.itemconfig(self.rectangles[self.index], outline="blue")

    def save_file(self):
        filename = filedialog.asksaveasfilename(defaultextension='.c', filetypes=[
            ('all files', '.*'), ('c code', '.c')])
        if not filename:
            return
        try:
            f = open(filename, "wt")
        except:
            print("cannot open file")
            return
        sp = []
        for i in range(256):
            image = self.images[i]
            for x in range(5):
                txt = ""
                for y in range(8):
                    color = "0" if image.get(x * 2, y * 2)[0] == 255 else "1"
                    txt += color
                txt = txt[::-1]
                sp.append("0x%s" % hexf(int(txt, 2)))
        f.write(START)
        txt = ""
        for i in range(256):
            b = sp[i * 5:i * 5 + 5]
            b = "\t" + ", ".join(b)
            if i != 255:
                b += ","
            b += "\t//%s\t%s\n" % (hexf(i), i)
            txt += b
        f.write(txt)
        f.write(END)
        f.close()
        print("save ok")

    def click(self, event):
        tag = self.canvas.find_withtag(CURRENT)
        if not tag:
            return
        tag = tag[0]
        if self.canvas.type(tag) == "rectangle" and tag in self.area:
            index = self.area.index(tag)
            image = self.images[self.index]
            x = int(index / 8)
            y = int(index % 8)
            if image.get(x * 2, y * 2)[0] == 255:
                self.putpixel(image, x, y, "#000")
                self.canvas.itemconfig(tag, fill="black")
            else:
                self.putpixel(image, x, y, "#fff")
                self.canvas.itemconfig(tag, fill="white")
        elif self.canvas.type(tag) == "image" and tag in self.indexs:
            index = self.indexs.index(tag)
            image = self.images[index]
            rectangle = self.rectangles[index]
            self.canvas.itemconfig(self.rectangles[self.index], outline="grey")
            self.index = index
            self.canvas.itemconfig(rectangle, outline="blue")
            self.canvas.itemconfig("INT", text=str(index))
            self.canvas.itemconfig("HEX", text=hexf(index))
            self.load(image)

    def load(self, image):
        i = 0
        for x in range(5):
            for y in range(8):
                color = "white" if image.get(
                    x * 2, y * 2)[0] == 255 else "black"
                self.canvas.itemconfig(self.area[i], fill=color)
                i += 1

    def putpixel(self, image, x, y, color):
        image.put(color, (x * 2, y * 2))
        image.put(color, (x * 2, y * 2 + 1))
        image.put(color, (x * 2 + 1, y * 2))
        image.put(color, (x * 2 + 1, y * 2 + 1))


root = Tk()
app = Application(master=root)
app.master.title("Font Editor")
app.master.resizable(width=FALSE, height=FALSE)
app.mainloop()
