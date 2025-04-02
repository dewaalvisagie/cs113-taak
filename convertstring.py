import stdio
import sys
import math


asciistring =""
asciinumber = 0
string = input("enter string: ")
binarynumba = ""
for i in range(len(string)):
    asciistring +=str(ord(string[i]))
    asciinumber += ord(string[i])
stdio.writeln(asciistring)
stdio.writeln(str(asciinumber))
v = 1 
while v<=asciinumber//2:
    v*=2
while v>0:
    if asciinumber<v:
      binarynumba +="0"  
    else:
        binarynumba +="1"
        asciinumber-=v
    v//=2
stdio.writeln(binarynumba)