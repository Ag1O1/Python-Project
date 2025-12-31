from convertions import decimal_to_binary
#
def decimal_list_to_binary(minterms,number_of_variables):
    minterms = [decimal_to_binary(x) for x in minterms]
    for i in range(len(minterms)):
        minterms[i] = minterms[i].zfill(number_of_variables)
    return minterms

def merge(a, b):
    diff = 0
    res = ""

    for i in range(len(a)):
        if a[i] != b[i]:
            diff += 1
            res = res + "-"
        else:
            res = res + a[i]
    if diff == 1:
        return res
    return None


def minterm_to_expression(minterms,number_of_variables):
    original_minterms = minterms.copy()
    minterms = decimal_list_to_binary(minterms,number_of_variables)
    all_primes = set()

    while True:
        groups = []
        merged = set()
        used = set()

        while len(groups) < number_of_variables+1:
            groups.append([])

        for s in minterms:
            number_of_ones = 0
            for c in s:
                if c == '1':
                    number_of_ones += 1
            groups[number_of_ones].append(s)

        print(minterms)
        print(groups)

        for i in range(len(groups)-1):
            for a in groups[i]:
                for b in groups[i+1]:
                    m = merge(a,b)
                    if m:
                        used.add(a)
                        used.add(b)
                        merged.add(m)

        primes = set(minterms) - used
        all_primes.update(primes)
        print(merged)
        print(primes)

        if not merged:
            break
        minterms = list(merged)

    print("All_primes: ",all_primes)
    best_primes = select_best_primes(all_primes,original_minterms,number_of_variables)
    final_res = binary_to_expression(best_primes ,number_of_variables)
    if len(best_primes) == 1 and (best_primes[0] == '-'*number_of_variables):
        return "1"
    else: return final_res

def binary_to_expression(binary_expression,number_of_variables):
    # Generates letters depending on number_of_variables (A,B,C...)
    vars = [chr(i) for i in range(65, 65 + number_of_variables)]
    expression = ""
    for bin in binary_expression:
        for i in range(len(bin)):
            if bin[i] == "0":
                expression += vars[i] + "'"
            elif bin[i] == "1":
                expression += vars[i]
        expression += " + "
    expression = expression[0:len(expression)-3]
    return expression

def covers(prime, decimal_minterm,number_of_variables):
    binary_minterm = decimal_to_binary(decimal_minterm).zfill(number_of_variables)
    for i in range(len(prime)):
        if prime[i] != "-" and prime[i] != binary_minterm[i]:
            return False
    return True

def select_best_primes(all_primes, original_decimal_minterms,number_of_variables):
    remaining_minterms = set(original_decimal_minterms)
    final_primes = []

    while remaining_minterms:
        best_prime = None
        covered_by_best = set()

        for prime in all_primes:
            currently_covered = {m for m in remaining_minterms if covers(prime, m,number_of_variables)}

            if best_prime is None or len(currently_covered) > len(covered_by_best):
                best_prime = prime
                covered_by_best = currently_covered

        if best_prime:
            final_primes.append(best_prime)
            remaining_minterms -= covered_by_best
        else:
            break

    return final_primes
