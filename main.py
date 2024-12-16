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
    
    operators = {"+", "-", "/", "X", "*", "^"}  # Notez que X est traité comme un opérateur.
    
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
