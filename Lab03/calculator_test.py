import unittest
from calculator import Calculator
import math


class ApplicationTest(unittest.TestCase):
    calculator = Calculator()
    param_list = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]

    def test_add(self):
        for i, j in self.param_list:
            self.assertEqual(self.calculator.add(i, j), i + j)
        self.assertRaises(TypeError, self.calculator.add(1, "1"))

    def test_divide(self):
        for i, j in self.param_list:
            self.assertEqual(self.calculator.divide(i, j), i / j)
        self.assertRaises(ZeroDivisionError, self.calculator.divide(1, 0))

    def test_sqrt(self):
        for _, j in self.param_list:
            self.assertEqual(self.calculator.sqrt(j), math.sqrt(j))
        self.assertRaises(TypeError, self.calculator.sqrt("1"))

    def test_exp(self):
        for _, j in self.param_list:
            self.assertEqual(self.calculator.exp(j), math.exp(j))
        self.assertRaises(TypeError, self.calculator.exp("1"))


if __name__ == '__main__':
    unittest.main()
