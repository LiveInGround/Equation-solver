import math

def is_int(input:str):
    for i in input:
        if i in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]:
            continue
        else:
            return False
    return True

def parse_equation(input:str):
    left = []
    right = []
    equal = False
    char = ""
    index = 0
    
    operators = ("+", "-", "/", "X", "*")
    
    for i in input:
        if i == "=" and equal:
            raise Exception("More than 1 ´=´ in the equation !")
        elif i == "=" and not(equal):
            equal = True
            continue
        elif i in operators:
            if equal:
                right.append(char)
                right.append(i)
            else:
                left.append(char)
                left.append(i)
            