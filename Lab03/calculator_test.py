import unittest
from calculator import Calculator
import math


class ApplicationTest(unittest.TestCase):
    calculator = Calculator()
    param_list = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    raise_param = (1, "1")

    def test_add(self):
        for i, j in self.param_list:
            self.assertEqual(self.calculator.add(i, j), i + j)
        with self.assertRaises(TypeError):
            self.calculator.add(
                self.raise_param[0],
                self.raise_param[1]
            )

    def test_divide(self):
        for i, j in self.param_list:
            self.assertEqual(self.calculator.divide(i, j), i / j)
        with self.assertRaises(TypeError):
            self.calculator.divide(
                self.raise_param[0],
                self.raise_param[1]
            )

    def test_sqrt(self):
        for _, j in self.param_list:
            self.assertEqual(self.calculator.sqrt(j), math.sqrt(j))
        with self.assertRaises(TypeError):
            self.calculator.sqrt(self.raise_param[1])

    def test_exp(self):
        for _, j in self.param_list:
            self.assertEqual(self.calculator.exp(j), math.exp(j))
        with self.assertRaises(TypeError):
            self.calculator.exp(self.raise_param[1])


if __name__ == '__main__':
    unittest.main()
