class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        inp = input("what command would you like to perform")
        if inp == "Add":
            print(self.Add(a, b))
        elif inp == "Subtract":
            print(self.Subtract(a, b))
        elif inp == "Multiply":
            print(self.Multiply(a, b))
        elif inp == "Divide":
            print(self.Divide(a, b))
        else:
            print("Error.")
    def Add(self, a, b):
        return a + b
    def Subtract(self, a, b):
        return a - b
    def Multiply(self, a, b):
        return a * b
    def Divide(self, a, b):
        return a / b
c = Calculator(1, 2)
