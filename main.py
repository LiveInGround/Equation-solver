# EqSolver by lig

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
            equal = True
            if char.strip():
                (right if equal else left).append(char.strip())
                char = ""
        elif i in operators:
            if char.strip():
                (right if equal else left).append(char.strip())
            (right if equal else left).append(i)
            char = ""
        else:
            char += i
    
    if char.strip():
        (right if equal else left).append(char.strip())

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
        if not(i in operators):
            try:
                sign = right[i-1]
            except IndexError:
                sign = "+"
            left.append({"+":"-", "-":"+"}[sign])
            left.append(i)
            
    x2 = 0
    x = 0
    c = 0
    for i, j in enumerate(left):
        if not("x" in j):
            c += {"+":1, "-":-1}[left[i-1]] * j
            
        else:
            ...
