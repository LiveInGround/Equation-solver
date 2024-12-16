import math

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
            ...