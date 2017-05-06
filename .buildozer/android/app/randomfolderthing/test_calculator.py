from unittest import TestCase
from randomfolderthing.Solver import Calculator

class TestCalculator(TestCase):
    def test_Add(self):
        c = Calculator(1, 2)
        self.assertRaises(Exception, c.Add(1, 2))


    def test_Subtract(self):
        self.fail()

    def test_Multiply(self):
        self.fail()

    def test_Divide(self):
        self.fail()
