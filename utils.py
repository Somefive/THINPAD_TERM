import binascii
__author__ = 'Somefive'


def bin2hexstr_16bit(bin_num):
    raw = str(binascii.hexlify(bin_num))[2:-1].upper()
    return raw[2:4]+raw[0:2]


def bin2binstr_16bit(bin_num):
    raw = padstr(bin(int(str(binascii.hexlify(bin_num))[2:-1].upper(), 16))[2:], 16)
    return raw[8:16]+raw[0:8]


def hexstr2bin_16bit(hex_num):
    return bytes.fromhex(hex_num[2:4])+bytes.fromhex(hex_num[0:2])


def padstr(raw_str, size):
    pad_size = size-len(raw_str)
    new_str = raw_str
    for index in range(0, pad_size):
        new_str = "0"+new_str
    return new_str


def extend_16bit(immediate, sign=True):
    pad_size = 16-len(immediate)
    if sign:
        pad_unit = immediate[0:1]
    else:
        pad_unit = "0"
    result = immediate
    for index in range(0, pad_size):
        result = pad_unit+result
    return result


def instruction2reg(instruction):
    return "R"+str(int(instruction[0:3], 2))


def reg2instruction(reg):
    return padstr(bin(int(reg[-1:]))[2:], 3)
