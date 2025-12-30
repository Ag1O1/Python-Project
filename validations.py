### AA
def validate_hex(hex:str) -> bool:
    for c in hex.lower():
        if c not in "abcdef0123456789":
            return False
    return True

def validate_octal(oct:str) -> bool:
    for c in oct:
        if c not in "01234567":
            return False
    return True

### OA
def validate_binary(binary):
    if binary == "":
        return False

    for digit in binary:
        if digit != '0' and digit != '1':
            return False

    return True

def validate_decimal(decimal):
    if decimal == "":
        return False

    for digit in decimal:
        if digit < '0' or digit > '9':
            return False

    return True
