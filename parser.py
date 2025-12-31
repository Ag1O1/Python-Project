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
        # Detect for bin,oct,hex patterns (0x,0o,0b)
        if c == "0" and i+1 < len(string) and string[i+1] in "box":
            prefix = string[i:i+2]
            i += 2
            num = prefix
            while i < len(string) and (string[i].isdigit() or string[i] in "ABCDEFabcdef"):
                num += string[i]
                i += 1
            tokens.append(num)
        # Numbers
        elif c.isdigit():
            number += c
            i += 1
        # Operators
        elif c in  "+-*/^()":
            # Flush number
            if number:
                tokens.append(int(number))
                number = ""
            tokens.append(c)
            i += 1
        # Spaces
        elif c == " ":
            # Flush number
            if number:
                tokens.append(int(number))
                number = ""
            i += 1
        else:
            # Raise vlaue error if character is none of the symbols above
            raise ValueError("invalid character")
    # Flush number
    if number:
        tokens.append(int(number))
    print(tokens)
    return tokens

def evaluate(tokens):
    i = 0
    while i < len(tokens):
        # Unary minus
        if tokens[i] == "-":
            # If previous token is an operator, then a minus is found then it is unary
            if i == 0 or str(tokens[i-1]) in "^*/+-(":
                if isinstance(tokens[i+1], (float, int)):
                    val = tokens[i+1]
                    tokens[i:i+2] = [-val]
                    i = max(0, i - 1)
                    continue
        i += 1

    i = 0
    while i < len(tokens):
        # Evaulate exponents
        if isinstance(tokens[i], str) and tokens[i] in "^":
            res = operate(tokens[i-1], tokens[i+1], tokens[i])
            tokens[i-1:i+2] = [res]
            i -= 1
        else:
            i += 1

    i = 0
    while i < len(tokens):
        # Evaulate multiplication/division
        if isinstance(tokens[i], str) and tokens[i] in "*/":
            res = operate(tokens[i-1], tokens[i+1], tokens[i])
            tokens[i-1:i+2] = [res]
            i -= 1
        else:
            i += 1

    i = 0
    while i < len(tokens):
        # Evaulate plus/minus
        if isinstance(tokens[i], str) and tokens[i] in "+-":
            res = operate(tokens[i-1], tokens[i+1], tokens[i])
            tokens[i-1:i+2] = [res]
            i -= 1
        else:
            i += 1
    return tokens

# Evaluate parantheses first
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

# Evaluate bin,hex,oct conversions
def evaluate_conversions(tokens):
    while any(isinstance(t, str) and t.startswith(("0b","0o","0x")) for t in tokens):
        for i in range(len(tokens)):
            if validate_decimal(str(tokens[i])): continue
            # Evaluate binary
            if tokens[i].startswith("0b"):
                # Raise error if binary value is invalid
                if not validate_binary(tokens[i][2:len(tokens[i])]):
                    raise ValueError("invalid binary value")
                num = tokens[i][2:len(tokens[i])]
                num = convert_to_decimal(num,"bin")
                tokens[i] = num
            # Evaluate octal
            elif tokens[i].startswith("0o"):
                # Raise error if octal value is invalid
                if not validate_octal(tokens[i][2:len(tokens[i])]):
                    raise ValueError("invalid octal value")
                num = tokens[i][2:len(tokens[i])]
                num = convert_to_decimal(num,"oct")
                tokens[i] = num
            # Evaluate hex
            elif tokens[i].startswith("0x"):
                # Raise error if hex value is invalid
                if not validate_hex(tokens[i][2:len(tokens[i])]):
                    raise ValueError("invalid hexadecimal value")
                num = tokens[i][2:len(tokens[i])]
                num = convert_to_decimal(num,"hex")
                tokens[i] = num
    return tokens

def calc(string):
    # Handle empty inputs
    if string == "":
        raise SyntaxError("empty input")
    tokens = tokenize(string)
    res = evaluate_parentheses(evaluate_conversions(tokens))
    if len(res) == 1:
        return res[0]
    else:
        # Handle missing operator, detected if result list doesn't collapse into one value
        raise SyntaxError("missing operator between values")
