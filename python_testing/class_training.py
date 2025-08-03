class Calculator:
    def __init__(self, value):
        self.value = value

    def add(self,x):
        self.value += x

    @classmethod
    def from_string(cls,string):
        return cls(int(string))
    
    @staticmethod
    def multiply(x, y):
        return x * y
    


calc = Calculator(10)
calc.add(5)
print(calc.value)  # Output: 15

calc2 = Calculator.from_string("20")
print(calc2.value)  # Output: 20

print(Calculator.multiply(3, 4))  # Output: 12
