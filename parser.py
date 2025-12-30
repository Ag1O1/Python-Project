from validations import validate_decimal, validate_binary, validate_hex, validate_octal
from convertions import convert_to_decimal, decimal_to_base
def operate(num1,num2,operation):
    if operation == "+":
        num1 = num1 + num2
    elif operation == "-":
        num1 = num1 - num2
    elif operation == "*":
        num1 = num1 * num2
    elif operation == "^":
        num1 = num1 ** num2
    elif operation == "/":
        if num2 == 0:
            raise ValueError("division by zero")
        num1 = num1 // num2
    else:
        raise ValueError("invalid operation")
    return num1

def tokenize(string):
    tokens = []
    number = ""
    i = 0
    while i < len(string):
        c = string[i]
        if c == "0" and i+1 < len(string) and string[i+1] in "box":
            prefix = string[i:i+2]
            i += 2
            num = prefix
            while i < len(string) and (string[i].isdigit() or string[i] in "ABCDEFabcdef"):
                num += string[i]
                i += 1
            tokens.append(num)
        elif c.isdigit():
            number += c
            i += 1
        elif c in  "+-*/^()":
            if number:
                tokens.append(int(number))
                number = ""
            tokens.append(c)
            i += 1
        elif c == " ":
            if number:
                tokens.append(int(number))
                number = ""
            i += 1
        else:
            raise ValueError("invalid character")
    if number:
        tokens.append(int(number))
    print(tokens)
    return tokens

def evaluate(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == "-":
            if i == 0 or str(tokens[i-1]) in "^*/+-(":
                if isinstance(tokens[i+1], (float, int)):
                    val = tokens[i+1]
                    tokens[i:i+2] = [-val]
                    i = max(0, i - 1)
                    continue
        i += 1

    i = 0
    while i < len(tokens):
        if isinstance(tokens[i], str) and tokens[i] in "^":
            res = operate(tokens[i-1], tokens[i+1], tokens[i])
            tokens[i-1:i+2] = [res]
            i -= 1
        else:
            i += 1

    i = 0
    while i < len(tokens):
        if isinstance(tokens[i], str) and tokens[i] in "*/":
            res = operate(tokens[i-1], tokens[i+1], tokens[i])
            tokens[i-1:i+2] = [res]
            i -= 1
        else:
            i += 1

    i = 0
    while i < len(tokens):
        if isinstance(tokens[i], str) and tokens[i] in "+-":
            res = operate(tokens[i-1], tokens[i+1], tokens[i])
            tokens[i-1:i+2] = [res]
            i -= 1
        else:
            i += 1
    return tokens

def evaluate_parentheses(tokens):
    while "(" in tokens:
        start = 0
        for i in range(len(tokens)):
            if (i == len(tokens)-1 and  not tokens[i] == ")") or tokens[len(tokens)-1] == "(":
                raise SyntaxError("no matching closing bracket")
            elif tokens[i] == "(":
                start = i
            elif tokens[i] == ")":
                res = evaluate(tokens[start+1:i])
                tokens[start:i+1] = res
                break
    return evaluate(tokens)

def evaluate_conversions(tokens):
    while any(isinstance(t, str) and t.startswith(("0b","0o","0x")) for t in tokens):
        for i in range(len(tokens)):
            if validate_decimal(str(tokens[i])): continue
            if tokens[i].startswith("0b"):
                if not validate_binary(tokens[i][2:len(tokens[i])]):
                    raise ValueError("invalid binary value")
                num = tokens[i][2:len(tokens[i])]
                num = convert_to_decimal(num,"bin")
                tokens[i] = num
            elif tokens[i].startswith("0o"):
                if not validate_octal(tokens[i][2:len(tokens[i])]):
                    raise ValueError("invalid octal value")
                num = tokens[i][2:len(tokens[i])]
                num = convert_to_decimal(num,"oct")
                tokens[i] = num
            elif tokens[i].startswith("0x"):
                if not validate_hex(tokens[i][2:len(tokens[i])]):
                    raise ValueError("invalid hexadecimal value")
                num = tokens[i][2:len(tokens[i])]
                num = convert_to_decimal(num,"hex")
                tokens[i] = num
    return tokens

def calc(string):
    tokens = tokenize(string)
    res = evaluate_parentheses(evaluate_conversions(tokens))[0]
    return res
