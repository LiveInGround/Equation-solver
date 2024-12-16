# EqSolver by lig

import math

operators = {"+", "-", "/", "X", "*", "^"}
def is_float(input_str: str) -> bool:
    try:
        float(input_str)
        return True
    except ValueError:
        return False

def parse_equation(input_str: str):
    left = []
    right = []
    equal = False
    char = ""
    

    
    for i in input_str:
        if i == "=":
            if equal:
                raise ValueError("More than one '=' in the equation!")
            
            if char.strip():
                (right if equal else left).append(char.strip())
                char = ""
            equal = True
        elif i in operators:
            if char.strip():
                (right if equal else left).append(char.strip())
            (right if equal else left).append(i)
            char = ""
        else:
            char += i
    
    if char.strip():
        (right if equal else left).append(char.strip())

    for side in (left, right):
        if side and side[0] not in operators:
            side.insert(0, "+")

    if not equal:
        raise ValueError("No '=' found in the equation!")

    def process_side(side):
        processed = []
        skip = False
        for i, item in enumerate(side):
            if skip:
                skip = False
                continue
            if item == "^" and i > 0 and i < len(side) - 1:
                processed[-1] = f"{processed[-1]}^{side[i + 1]}"
                skip = True
            elif is_float(item):
                processed.append(float(item))
            else:
                processed.append(item)
        return processed

    return process_side(left), process_side(right)

def solve_equation(input:str) -> None|tuple:
    left, right = parse_equation(input)
    
    for i, j in enumerate(right):
        if not(j in operators):
            if i - 1 < 0:
                sign = "+"
            else:
                sign = right[i-1]
            left.append({"+":"-", "-":"+"}[sign])
            left.append(j)
            
    x2 = 0
    x = 0
    c = 0
    for i, j in enumerate(left):
        if not("x" in str(j)) and not(j in operators):
            c += {"+":1, "-":-1}[left[i-1]] * j
            
        elif not(j in operators):
            char = ""
            puissance_v = ""
            puissance = False
            for k in j:
                if k == "x":
                    continue
                elif k == "^" and not(puissance):
                    puissance = True
                elif k == "^" and puissance:
                    raise Exception()
                else:
                    if puissance:
                        puissance_v += k
                    else:
                        char += k
            value = float(char)
            if puissance_v != "":
                p_n = int(puissance_v)
            else:
                p_n = 1
            
            if p_n == 0:
                c += value * {"+":1, "-":-1}[left[i-1]]
            elif p_n == 1:
                x += value * {"+":1, "-":-1}[left[i-1]]
            elif p_n == 2:
                x2 += value * {"+":1, "-":-1}[left[i-1]]
            else:
                raise Exception("More than 2 degrees are not supported.")

    print(x2)
    print(x)
    print(c)

    if x2 != 0:
        delta = x ** 2 - 4*x2*c
        if delta < 0:
            print(delta)
            return None
        elif delta > 0:
            s1 = (-x - math.sqrt(delta)) /2 * x2
            s2 = (-x + math.sqrt(delta)) /2 * x2
            if s1 > s2:
                return (s2, s1)
            else:
                return (s1, s2)
        else:
            return ((-x - math.sqrt(delta)), )
    else:
        assert x != 0
        return (-c/x, )
        
