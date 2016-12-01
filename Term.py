import serial
import serial.serialutil
from time import clock
from translation import *

__author__ = 'Somefive'

t = serial.Serial
while True:
    com = input("please choose the COM:")
    try:
        t = serial.Serial(com, parity=serial.PARITY_ODD)
        break
    except serial.serialutil.SerialException:
        print("cannot open the com")

skip = input("Skip Ok or not?[Y/N]")
if skip != "Y":
    # wait for hello
    n = t.read(4)
    opening = n.decode("ascii")
    print(opening)

# start running
while True:
    print(">>", end="")
    ops = input().split(' ')
    op = ops[0]
    byteop = bytes.fromhex(hex(ord(op))[2:])
    if op is "R":
        t.write(byteop)
        for i in range(0, 6):
            print("Reg"+str(i)+":", end='')
            reg = t.read(2)
            print(str(binascii.hexlify(reg))[2:-1])
    elif op is "D":
        if ops.__len__() > 2:
            addr = padstr(ops[1], 4)
            number = padstr(ops[2], 4)
        else:
            addr = "8000"
            number = "0001"
        count = int(number, 16)
        t.write(byteop)
        t.write(hexstr2bin_16bit(addr))
        t.write(hexstr2bin_16bit(number))
        for i in range(0, count):
            data = t.read(2)
            cur_addr = hex(int(addr, 16)+i)[2:]
            cur_addr = padstr(cur_addr, 4)
            print("["+cur_addr+"]\t"+bin2hexstr_16bit(data))
    elif op is "U":
        if ops.__len__() > 2:
            addr = padstr(ops[1], 4)
            number = padstr(ops[2], 4)
        else:
            addr = "8000"
            number = "0001"
        if ops.__len__() > 4 and ops[3] == "-f":
            fp = open(ops[4], "w")
        count = int(number, 16)
        t.write(byteop)
        t.write(hexstr2bin_16bit(addr))
        t.write(hexstr2bin_16bit(number))
        for i in range(0, count):
            data = t.read(2)
            cur_addr = hex(int(addr, 16)+i)[2:]
            cur_addr = padstr(cur_addr, 4)
            result = bit2lang(bin2binstr_16bit(data))
            if result == "":
                result = "-- Unknown Instruction --"
            print("["+cur_addr+"]\t"+result)
            if ops.__len__() > 4 and ops[3] == "-f":
                fp.write(result+"\n")
        if ops.__len__() > 4 and ops[3] == "-f":
            fp.close()
    elif op is "A":
        if ops.__len__() > 1:
            addr = padstr(ops[1], 4)
        else:
            addr = "4000"
        file_flag = (ops.__len__() > 3 and ops[2] == "-f")
        if file_flag:
            fp = open(ops[3], "r")
        t.write(byteop)
        count = 0
        cur_addr = padstr(hex(int(addr, 16)+count)[2:], 4)
        if file_flag:
            lang = fp.readline().replace('\n', '')
            print("["+cur_addr+"]\t"+lang)
        else:
            lang = input("["+cur_addr+"]\t")
        while lang != "":
            ins = lang2bit(lang)
            if ins == "":
                print("Error Input!")
            else:
                t.write(hexstr2bin_16bit(cur_addr))
                t.write(hexstr2bin_16bit(padstr(hex(int(ins, 2))[2:], 4)))
            count += 1
            cur_addr = padstr(hex(int(addr, 16)+count)[2:], 4)
            if file_flag:
                lang = fp.readline()
                print("["+cur_addr+"]\t"+lang)
            else:
                lang = input("["+cur_addr+"]\t")
        t.write(hexstr2bin_16bit("0000"))
    elif op is "G":
        if ops.__len__() > 1:
            addr = padstr(ops[1], 4)
        else:
            addr = "4000"
        if ops.__len__() > 2 and ops[2] == "-t":
            start = clock()
        t.write(byteop)
        t.write(hexstr2bin_16bit(addr))
        n = t.read(1)
        while str(binascii.hexlify(n))[2:-1] != "07":
            print(n.decode("ascii"), end="")
            n = t.read(1)
        print()
        if ops.__len__() > 2 and ops[2] == "-t":
            delta = (clock() - start)*1000
            print("Time Used: "+str(delta)+" ms")




# t.write(bytes.fromhex('ff'))

# end Term
t.close()
