import re
from utils import *
__author__ = 'Somefive'

InstructionPatterns = {
    "ADDIU":    re.compile('01001([01]{3})([01]{8})'),
    "ADDIU3":   re.compile('01000([01]{3})([01]{3})0([01]{4})'),
    "ADDSP":    re.compile('01100011([01]{8})'),
    "ADDU":     re.compile('11100([01]{3})([01]{3})([01]{3})01'),
    "AND":      re.compile('11101([01]{3})([01]{3})01100'),
    "B":        re.compile('00010([01]{11})'),
    "BEQZ":     re.compile('00100([01]{3})([01]{8})'),
    "BNEZ":     re.compile('00101([01]{3})([01]{8})'),
    "BTEQZ":    re.compile('01100000([01]{8})'),
    "CMP":      re.compile('11101([01]{3})([01]{3})01010'),
    "JR":       re.compile('11101([01]{3})00000000'),
    "LI":       re.compile('01101([01]{3})([01]{8})'),
    "LW":       re.compile('10011([01]{3})([01]{3})([01]{5})'),
    "LW_SP":    re.compile('10010([01]{3})([01]{8})'),
    "MFIH":     re.compile('11110([01]{3})00000000'),
    "MFPC":     re.compile('11101([01]{3})01000000'),
    "MTIH":     re.compile('11110([01]{3})00000001'),
    "MTSP":     re.compile('01100100([01]{3})00000'),
    "NOP":      re.compile('0000100000000000'),
    "OR":       re.compile('11101([01]{3})([01]{3})01101'),
    "SLL":      re.compile('00110([01]{3})([01]{3})([01]{3})00'),
    "SRA":      re.compile('00110([01]{3})([01]{3})([01]{3})11'),
    "SUBU":     re.compile('11100([01]{3})([01]{3})([01]{3})11'),
    "SW":       re.compile('11011([01]{3})([01]{3})([01]{5})'),
    "SW_SP":    re.compile('11010([01]{3})([01]{8})'),
    "MOVE":     re.compile('01111([01]{3})([01]{3})00000'),
    "SLLV":     re.compile('11101([01]{3})([01]{3})00100'),
    "ADDSP3":   re.compile('00000([01]{3})([01]{8})'),
    "CMPI":     re.compile('01110([01]{3})([01]{8})'),
    "NEG":      re.compile('11101([01]{3})([01]{3})01011'),
}

InstructionStructures = {
    "ADDIU":    ('01001(rx)(im)', 8),
    "ADDIU3":   ('01000(rx)(ry)0(im)', 4),
    "ADDSP":    ('01100011(im)', 8),
    "ADDU":     ('11100(rx)(ry)(rz)01', 0),
    "AND":      ('11101(rx)(ry)01100', 0),
    "B":        ('00010(im)', 11),
    "BEQZ":     ('00100(rx)(im)', 8),
    "BNEZ":     ('00101(rx)(im)', 8),
    "BTEQZ":    ('01100000(im)', 8),
    "CMP":      ('11101(rx)(ry)01010', 0),
    "JR":       ('11101(rx)00000000', 0),
    "LI":       ('01101(rx)(im)', 8),
    "LW":       ('10011(rx)(ry)(im)', 5),
    "LW_SP":    ('10010(rx)(im)', 8),
    "MFIH":     ('11110(rx)00000000', 0),
    "MFPC":     ('11101(rx)01000000', 0),
    "MTIH":     ('11110(rx)00000001', 0),
    "MTSP":     ('01100100(rx)00000', 0),
    "NOP":      ('0000100000000000', 0),
    "OR":       ('11101(rx)(ry)01101', 0),
    "SLL":      ('00110(rx)(ry)(im)00', 3),
    "SRA":      ('00110(rx)(ry)(im)11', 3),
    "SUBU":     ('11100(rx)(ry)(rz)11', 0),
    "SW":       ('11011(rx)(ry)(im)', 5),
    "SW_SP":    ('11010(rx)(im)', 8),
    "MOVE":     ('01111(rx)(ry)00000', 0),
    "SLLV":     ('11101(rx)(ry)00100', 0),
    "ADDSP3":   ('00000(rx)(im)', 8),
    "CMPI":     ('01110(rx)(im)', 8),
    "NEG":      ('11101(rx)(ry)01011', 0),
}


def bit2lang(instruction):
    result = ""
    for code in InstructionPatterns.keys():
        match = InstructionPatterns[code].match(instruction)
        if match:
            result = code
            for i in range(1, len(match.groups())+1):
                if len(match.group(i)) == 3 and (i <= 2 or (code != "SRA" and code != "SLL")):
                    result = result + " " + instruction2reg(match.group(i))
                else:
                    result = result + " " + "0x" + padstr(hex(int(extend_16bit(match.group(i)), 2))[2:], 4)[2:4]
            break
    return result.upper().replace('X', 'x')


def lang2bit(lang):
    units = lang.split(' ')
    if units[0] not in InstructionStructures.keys():
        return ""
    result = InstructionStructures[units[0]][0]
    if len(units) > 1 and units[1].startswith('R'):
        result = result.replace("(rx)", reg2instruction(units[1]))
        if len(units) > 2 and units[2].startswith('R'):
            result = result.replace("(ry)", reg2instruction(units[2]))
            if len(units) > 3 and units[3].startswith('R'):
                result = result.replace("(rz)", reg2instruction(units[3]))
    if len(units) > 1 and not units[-1].startswith('R'):
        binstr = padstr(bin(int(units[-1], 16))[2:], InstructionStructures[units[0]][1])
        binstr = extend_16bit(binstr, (units[0] != "LI"))
        result = result.replace("(im)", binstr[-InstructionStructures[units[0]][1]:])
    return result
