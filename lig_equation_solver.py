# An Equation Solver by LiveInGround
# This code is under the MIT License.
# You can find the license in the LICENSE file or at the following URL: https://opensource.org/licenses/MIT
# There will be future updates to this code, so stay tuned!

import math
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

operators = {"+", "-", "/", "X", "*", "^"}
def is_float(input_str: str) -> bool:
    """Check if a string can be converted as a float."""
    try:
        float(input_str)
        return True
    except ValueError:
        return False

def reduce(*args: tuple[int, int]) -> list[tuple[int, int]]:
    """This will be implemented in a future update. It will reduce the terms of the equation."""
    raise Exception("This function is not ready yet.")
    terms = defaultdict(int)

    for coef, exp in args:
        terms[exp] += coef

    return sorted(((coef, exp) for exp, coef in terms.items() if coef != 0), key=lambda x: -x[1])

def parse_equation(input_str: str) -> tuple[list[str], list[str]]:
    """This function analyse the given string and return a tuple of two lists, the left and right side of the equation."""
    if not input_str:
        raise ValueError("Empty string")
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

def solve_equation(input:str, show=False) -> None|tuple[float, float|complex|str|None, float|complex|str|None]:
    """This function solve the given equation and return the solutions.
    Args:
        input (str): The equation to solve.
        show (bool): If True, the graph will be saved as an image named graph.png."""
    
    left, right = parse_equation(input)
    
    for i, j in enumerate(right):
        if not(j in operators):
            if i - 1 < 0:
                sign = "+"
            else:
                sign = right[i-1]
            left.append({"+":"-", "-":"+"}[sign])
            left.append(j)

    """NOTE : 
    The following variables are not named as the exact way.
    In an equation like ax^3 + bx^2 + cx + d = 0, x3 is a, x2 is b, x is c and c is d."""

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
            if char == "":
                char = 1
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
                raise Exception("More than degree 3 are not supported.")

    def f(image):
        return x3 * image ** 3 + x2 * image ** 2 + x * image + c

    alpha = -(x / (2 * x2)) if x2 != 0 else 0
    beta = abs((x ** 2 - 4 * x2 * c) / (2 * x2)) if x2 != 0 else 10

    x_ = np.linspace(int(round(alpha - beta, 0)), int(round(alpha + beta, 0)), 500)
    y = f(x_)

    def g(img):
        return 0 * img

    y2 = g(x_)

    fig, ax = plt.subplots()
    ax.plot(x_, y, label=f"f(x)={x3}x^3+{x2}x^2+{x}x+{c}")
    ax.plot(x_, y2, label="g(x)=0")

    solutions = []

    issue = False

    if x3 != 0:
        raise Exception("Degree 3 is currently bugged, it will be awaiable in a future update.")
        p = (x2 ** 2 - 3 * x3 * c) / (3 * x3 ** 2)
        q = (2 * x2 ** 3 - 9 * x3 * x2 * c + 27 * x3 ** 2 * c) / (27 * x3 ** 3)

        d = (q / 2) ** 2 + (p / 3) ** 3

        if d > 0:
            sol = math.pow(-(q / 2) + math.sqrt(d), 1 / 3) + math.pow(-(q / 2) - math.sqrt(d), 1 / 3)
            solutions = [sol]
        elif d == 0:
            s1 = 2 * math.pow(-(q / 2), 1 / 3)
            s2 = -math.pow(-(q / 2), 1 / 3)
            solutions = [s1, s2]
        else:
            theta = math.acos(-q / (2 * math.sqrt((-p / 3) ** 3)))
            s1 = 2 * math.sqrt(-p / 3) * math.cos(theta / 3)
            s2 = 2 * math.sqrt(-p / 3) * math.cos((theta + 2 * math.pi) / 3)
            s3 = 2 * math.sqrt(-p / 3) * math.cos((theta + 4 * math.pi) / 3)
            solutions = [s1, s2, s3]

    elif x2 != 0:
        d = x ** 2 - 4 * x2 * c
        if d > 0:
            s1 = (-x - math.sqrt(d)) / (2 * x2)
            s2 = (-x + math.sqrt(d)) / (2 * x2)
            solutions = [s1, s2]
        elif d == 0:
            solutions = [-x / (2 * x2)]
        elif d < 0:
            s1 = (-x - 1j * math.sqrt(-d)) / (2 * x2)
            s2 = (-x + 1j * math.sqrt(-d)) / (2 * x2)
            solutions = [s1, s2]
    elif x != 0:
        solutions = [-c / x]
    else:
        solutions = ["Infinité solutions" if c == 0 else "No solution"]
        issue = True

    complex_mode = False
    for i in solutions:
        if isinstance(i, complex):
            complex_mode = True
    if not(complex_mode) and not(issue):
        for sol in solutions:
            ax.axvline(sol, color='r', linestyle='--', label=f"Solution: x={sol:.2f}")

        ax.set_title(input, size=14)
        plt.legend()
        if show:
            plt.savefig("graph.png")

    return tuple(solutions) if solutions else None
