import unittest
from util import left_most_bit

class LeftMostBitTest(unittest.TestCase):
    def test_left_most_bit(self):
        self.assertEquals(left_most_bit(0), -1)
        self.assertEquals(left_most_bit(1), 0)
        self.assertEquals(left_most_bit(4), 2)
        self.assertEquals(left_most_bit(5), 2)

    def test_quick_left_most_bit(self):
        from random import randrange
        for i in range(100):
            n = randrange(2**31)
            lmb = left_most_bit(n)
            if n == 0:
                self.assertEquals(lmb, -1)
            else:
                self.assertLessEqual(1 << lmb, n)
                self.assertLess(n, 1 << (lmb+1))

if __name__ == '__main__':
    unittest.main()
