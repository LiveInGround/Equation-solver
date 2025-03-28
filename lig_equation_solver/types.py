import math

class SquareRoot(object):
    def __init__(self, value):
        self.value=value
        
    def __repr__(self):
        return f"sqrt({value})")m 
        
    def calculate(self):
        return math.sqrt(self.value)
        
class Diff(object):
    def __init__(self, up, down):
        self.up = up
        self.down = down
        
    def __repr__(self):
        return f"DIFF({self.up};{self.down})"
        
    def calculate(self):
        ... # calculate up part
        ... # calculate down part
        
        ... # return up/down
        
def Pi(object):
    def __repr__(self):
        return "{pi}"
        
    def calculate(self):
        return math.pi