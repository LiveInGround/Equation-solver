import math

def is_float(input:str):
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
            
        elif i in operators:
            if equal:
                if is_float(char):
                    right.append(float(char))
                else:
                    right.append(char)
                right.append(i)
                
            else:
                if is_float(char):
                    left.append(float(char))
                else:
                    left.append(char)
                left.append(i)
        else:
            char += i
        index += 1
    
    assert equal
    
    for i, j in enumerate(left):
        if j == "x" and left[i+1] == "^":
            left[i] = f"x^{i+2}"
            del(left[i+1])
            del(left[i+1])
            
    for i, j in enumerate(right):
        if j == "x" and right[i+1] == "^":
            right[i] = f"x^{i+2}"
            del(right[i+1])
            del(right[i+1])
            
            
    return (left, right)