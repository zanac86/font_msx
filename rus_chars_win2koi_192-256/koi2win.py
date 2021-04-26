import os, sys, struct

def load_bin(fn):
    f=open(fn, "rb")
    s=f.read()
    b=struct.unpack("="+"B"*len(s), s)
    return [i for i in b]

koi=load_bin("b_koi8.bin")
win=load_bin("b_win.bin")

t=[]

'''

win 0xC0 -> rus'А' -> in koi8 at pos 0xE1

'''

ss=[]
for i in range(len(win)):
    c=win[i]
    ss.append("%d: %d" % (c, i))
    print("W:%02x -> K:%02x" % (c, i))

print("win2koi = { %s }" % ", ".join(ss[192:]))



