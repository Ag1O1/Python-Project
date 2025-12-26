import validations


### AA
def hex_to_decimal(hex:str):
    if not validations.validate_hex(hex):
        print("ERROR: Invalid hex")
        return
    res = 0
    hex = hex.lower()[::-1]
    for i in range(0,len(hex)):
        c = hex[i]
        if c == "a":
            res += 10*16**i
        elif c == "b":
            res += 11*16**i
        elif c == "c":
            res += 12*16**i
        elif c == "d":
            res += 13*16**i
        elif c == "e":
            res += 14*16**i
        elif c == "f":
            res += 15*16**i
        else:
            res += int(c)*16**i
    return res

def decimal_to_hex(dec:int):
    #if not validate_decimal(dec):
    #    print("Invalid number")
    #    return
    res = ""
    while dec != 0:
        remainder = dec % 16
        dec  = dec // 16
        if remainder == 10:
            res += "A"
        elif remainder == 11:
            res += "B"
        elif remainder == 12:
            res += "C"
        elif remainder == 13:
            res += "D"
        elif remainder == 14:
            res += "E"
        elif remainder == 15:
            res += "F"
        else:
            res += str(remainder)
    return res[::-1]


### OA
# binary to decimal
def binary_to_decimal(binary):
    decimal = 0
    power = 0

    for digit in reversed(binary):
        decimal += int(digit) * (2 ** power)
        power += 1

    return decimal


# decimal to octal
def decimal_to_octal(decimal):
    if decimal == 0:
        return "0"

    octal = ""

    while decimal > 0:
        remainder = decimal % 8
        octal = str(remainder) + octal
        decimal //= 8

    return octal


### OS
def octal_to_decimal(octalnum):
    decimal = 0

    for i in octalnum:
        decimal = decimal * 8 + int(i)

    return decimal

def convert_to_decimal(num:str,base:str):
    if base == "bin":
        return binary_to_decimal(num)
    elif base == "oct":
        return octal_to_decimal(num)
    elif base == "hex":
        return hex_to_decimal(num)
    elif base == "dec":
        return int(num)

# TODO: decimal_to_binary

def decimal_to_base(num:int,base:str):
    if base == "bin":
        print("ERROR not implemented")
        return
    elif base == "oct":
        return decimal_to_octal(num)
    elif base == "dec":
        return int(num)
    elif base == "hex":
        return decimal_to_hex(num)
    else:
        print("INVALID")
        return
