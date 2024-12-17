# EqSolver by lig

import math
import matplotlib.pyplot as plt
import numpy as np

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

def solve_equation(input:str, show=False) -> None|tuple:
    left, right = parse_equation(input)
    
    for i, j in enumerate(right):
        if not(j in operators):
            if i - 1 < 0:
                sign = "+"
            else:
                sign = right[i-1]
            left.append({"+":"-", "-":"+"}[sign])
            left.append(j)

    x3 = 0        
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
            elif p_n == 3:
                x3 += value * {"+":1, "-":-1}[left[i-1]]
            else:
                raise Exception("More than 2 degrees are not supported.")

    def f(image):
        return x3*image**3+x2*image**2+x*image+c
    
    alpha = -(x/2*x2)
    beta = -(x**2-4*x2*c)/2*x2

    x_ = np.linspace(int(round(alpha-10, 0)), int(round(alpha+10, 0)), int(round(beta+10, 0)) if beta > 0 else beta-10)
    y = f(x_)

    def g(img):
        return 0 * img
    
    y2 = g(x_)
    
    ig, ax = plt.subplots()
    ax.plot(x_, y, label=f"f(x)={x3}x^3+{x2}x^2+{x}x+{c}")
    ax.plot(x_, y2, label=f"g(x)=0")
    ax.set_title(input, size=14)
    plt.legend()
    plt.savefig("graph.png")

    if x3 != 0:
        p = (x2**2 - 3*x3*c) / (3*x3**2)
        q = (2*x2**3 - 9*x3*x2*c + 27*x3**2*c) / (27*x3**3)

        d = (q / 2) ** 2 + (p / 3) ** 3

        if d > 0:
            return math.pow(-(q/2)+math.sqrt(d), 3) + math.pow(-(q/2)-math.sqrt(d), 3)
        elif d == 0:
            s1 = 2*math.pow(-(q/2), 3)
            s2 = -math.pow(-(q/2), 3)

            if s1 < s2:
                return (s1, s2)
            else:
                return (s2, s1)
        else:
            theta = math.acos(-q / (2 * math.sqrt((-p / 3)**3)))
            s1 = 2 * math.sqrt(-p / 3) * math.cos(theta / 3)
            s2 = 2 * math.sqrt(-p / 3) * math.cos((theta + 2 * math.pi) / 3)
            s3 = 2 * math.sqrt(-p / 3) * math.cos((theta + 4 * math.pi) / 3)

            return (s1, s2, s3)

    elif x2 != 0:
        d = x ** 2 - 4*x2*c
        if d < 0:
            return None
        elif d > 0:
            s1 = (-x - math.sqrt(d)) /2 * x2
            s2 = (-x + math.sqrt(d)) /2 * x2
            if s1 > s2:
                return (s2, s1)
            else:
                return (s1, s2)
        else:
            return ((-x - math.sqrt(d)), )
    else:
        assert x != 0
        return (-c/x, )
        
solve_equation("-1x^2+5x=-2", True)