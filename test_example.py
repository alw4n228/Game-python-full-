
import unittest

def add(a, b):
    return a + b

class TestAddFunction(unittest.TestCase):
    
    def test_positive_numbers(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(3, 4), 7)

    def test_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)
        self.assertEqual(add(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()
                